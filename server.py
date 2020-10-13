import configparser
from datetime import datetime
from string import Template
import json
from flask import Flask, render_template, jsonify, request, redirect, flash, make_response
from flask_wtf.csrf import CSRFProtect, CSRFError
from time import time
from helper.getbmedata import getBMEData1
from helper.lights import LightsTimeForm, lights_parse

app = Flask(__name__)
CSRFProtect(app)
app.config.update(
    DEBUG=False,
    WTF_CSRF_ENABLED=False,
    SECRET_KEY='you-will-never-guess', )


@app.route("/myBME", methods=['POST', 'GET'])
def getTemps():
    global temp1, hum1, psi1
    if request.method == "GET":
        bmedata = getBMEData1()
        temp1 = bmedata[0]
        hum1 = bmedata[1]
        psi1 = bmedata[2]
    return jsonify(temp=temp1, hum=hum1, psi=psi1)


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


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
