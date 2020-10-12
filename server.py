import configparser
from datetime import datetime
from string import Template

from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_wtf.csrf import CSRFProtect, CSRFError

from helper.getbmedata import getBMEData1
from helper.lights import LightsTimeForm, lights_parse

app = Flask(__name__)
CSRFProtect(app)
app.config.update(
    DEBUG=True,
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


@app.route("/chart")
def chart():
    return render_template('chart.html', title="Chart")


@app.route("/index", methods=['GET', 'POST'])
@app.route("/")
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


@app.route("/lights_update", methods=['GET', 'POST'])
def delta_flash_msg():
    # delta_d = strfdelta(t1_diff, "%D")
    delta_hr = strfdelta(t1_diff, "%H")
    delta_min = strfdelta(t1_diff, "%M")
    delta_sec = strfdelta(t1_diff, "%S")

    if int(delta_hr) > 0:
        flash("Time was updated " + delta_hr + " hours, " + delta_min + " minutes, " + delta_sec + " seconds ago!",
              "warning")
    else:
        flash("Time was updated " + delta_min + " minutes, " + delta_sec + " seconds ago!",
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

    if form.validate_on_submit():
        lights_parse()
        delta_flash_msg()
        # print("Updated from file:", t1_updated_on)
        # print("Current time:", t1_current)
        flash("Time updated successfully!", "success")
        return redirect(request.url)

    return render_template('lights.html', title='Changing Light Schedule', form=form,
                           koo=t1_start_now, poo=t1_stop_now, diff=t1_diff)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
