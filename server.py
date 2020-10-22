#!/usr/bin/python3.5
import configparser
import json
from datetime import datetime, timedelta, timezone
from string import Template
from flask import Flask, render_template, jsonify, request, redirect, flash, make_response
from flask_wtf.csrf import CSRFProtect, CSRFError
from helper.ads import ads_sensor_01
from helper.getbmedata import getBMEData1
from helper.lights import LightsTimeForm, lights_parse
import sqlite3 as sql
import RPi.GPIO as GPIO
from datetime import datetime


app = Flask(__name__)
CSRFProtect(app)
app.config.update(
    DEBUG=False,
    WTF_CSRF_ENABLED=False,
    SECRET_KEY='you-will-never-guess', )


def mapper(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


@app.route("/moist", methods=['POST', 'GET'])
def moisture01():
    a = ads_sensor_01()
    val_moist = mapper(a, 1200, 2950, 100, 0)
    val_moist_str = str(val_moist)
    val_moist_str = str(val_moist_str + "%")
    return jsonify(moist=val_moist_str)


@app.route('/chart')
def hello_world():
    return render_template('chart.html')


@app.route('/live-data')
def live_data():
    bmedata = getBMEData1()
    bmedata = bmedata[0]
    old_time = datetime.now()
    new_time = old_time - timedelta(hours=5)
    data = (new_time.timestamp() * 1000, bmedata)

    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    print(response)
    return response


@app.cli.command()
def addtodb():
    """Add Inside temp to "temp.db"."""
    global temp_inside, hum_inside, psi_inside
    bmedata = getBMEData1()
    temp_inside = bmedata[0]
    hum_inside = bmedata[1]
    psi_inside = bmedata[2]
    with sql.connect("databases/temp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO temp_inside_db (temp_in,hum_in,psi_in) VALUES(?, ?, ?)",
                    (temp_inside, hum_inside, psi_inside))
        con.commit()
        print("Record successfully added:")
        query_Table = "SELECT * FROM temp_inside_db ORDER BY rowid DESC LIMIT 1;"
        queryResults = cur.execute(query_Table)

    for result in queryResults:
        print(result)


@app.route("/myBME", methods=['POST', 'GET'])
def getTemps():
    global temp1, hum1, psi1
    if request.method == "GET":
        bmedata = getBMEData1()
        temp1 = bmedata[0]
        hum1 = bmedata[1]
        psi1 = bmedata[2]
    return jsonify(temp=temp1, hum=hum1, psi=psi1)


@app.route("/moisture", methods=['GET', 'POST'])
def moisture():
    return render_template('moist.html', title="Moisture")


@app.route("/index")
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Main page")


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def lights_update_status():
    delta_d = strfdelta(t1_diff, "%D")
    delta_hr = strfdelta(t1_diff, "%H")
    delta_min = strfdelta(t1_diff, "%M")
    delta_sec = strfdelta(t1_diff, "%S")

    if int(delta_hr) > 0:
        flash("Last update was - " + delta_hr + " hr. " + delta_min + " min. " + delta_sec + " sec. ago!",
              "warning")
    elif int(delta_d) > 0:
        flash("Last update was - " + delta_d + " d. " + delta_hr + " hr. " + delta_min + " min. " + delta_sec + "sec. "
                                                                                                                "ago!",
              "warning")
    else:
        flash("Last update was - " + delta_min + " min. " + delta_sec + " sec. ago!",
              "warning")


@app.route("/lights", methods=['GET', 'POST'])
def addtime():
    global t1_diff

    form = LightsTimeForm()

    config = configparser.ConfigParser()
    config.read('static/configs/time_config.ini')

    t1_current_time_raw = str(datetime.now())[:-7]

    t1_start_now = config['LIGHTTIME_01']['START01']
    t1_stop_now = config['LIGHTTIME_01']['STOP01']
    t1_updated_on_raw = config['LIGHTTIME_01']['UPDATEDON']

    t1_updated_on = datetime.strptime(t1_updated_on_raw, "%Y-%m-%d %H:%M:%S")
    t1_current = datetime.strptime(t1_current_time_raw, "%Y-%m-%d %H:%M:%S")
    t1_diff = t1_current - t1_updated_on
    lights_update_status()
    if form.validate_on_submit():
        lights_parse()
        flash("Time updated successfully!", "success")
        return redirect(request.url)

    return render_template('lights.html', title='Changing Light Schedule', form=form,
                           koo=t1_start_now, poo=t1_stop_now)


@app.cli.command()
def check_time():
    """Check time and turn on GPIO 18"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)

    config = configparser.ConfigParser()
    config.read('static/configs/time_config.ini')
    now = datetime.now()
    time_now = now.strftime('%H:%M')

    [t_now_hr, t_now_min] = [int(time_now_minutes) for time_now_minutes in time_now.split(':')]
    time_now_minutes = timedelta(hours=t_now_hr, minutes=t_now_min)

    t1_start_now = config['LIGHTTIME_01']['START01'][:-3]

    [t1_start_hr, t1_start_min] = [int(t1_start_minutes) for t1_start_minutes in t1_start_now.split(':')]
    t1_start_minutes = timedelta(hours=t1_start_hr, minutes=t1_start_min)

    t1_stop_now = config['LIGHTTIME_01']['STOP01'][:-3]

    [t1_stop_hr, t1_stop_min] = [int(t1_stop_minutes) for t1_stop_minutes in t1_stop_now.split(':')]
    t1_stop_minutes = timedelta(hours=t1_stop_hr, minutes=t1_stop_min)

    t1_start_minutes_str = str(t1_start_minutes)
    time_now_minutes_str = str(time_now_minutes)
    t1_stop_minutes_str = str(t1_stop_minutes)

    if t1_start_minutes <= t1_stop_minutes:
        if t1_start_minutes <= time_now_minutes <= t1_stop_minutes:
            GPIO.output(18, GPIO.HIGH)
            print(
                "Time is in the set range. Turn lights on!: " + t1_start_minutes_str + "<=" + time_now_minutes_str +
                "<=" + t1_stop_minutes_str)
        else:
            GPIO.output(18, GPIO.LOW)
            print(
                "Current time is not in range!: " + t1_start_minutes_str + "<=" + time_now_minutes_str + "<=" +
                t1_stop_minutes_str)
    else:
        if t1_stop_minutes <= t1_start_minutes:
            if t1_stop_minutes <= time_now_minutes <= t1_start_minutes:
                GPIO.output(18, GPIO.LOW)
                print(
                    "Pm to AM. Time is in the set range. Turn lights on!: " + t1_start_minutes_str + "<=" +
                    time_now_minutes_str + "<=" + t1_stop_minutes_str)
            else:
                GPIO.output(18, GPIO.HIGH)
                print(
                    "PM to AM. Current time is not in range!: " + t1_start_minutes_str + "<=" + time_now_minutes_str +
                    "<=" + t1_stop_minutes_str)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
