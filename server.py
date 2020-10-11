from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_wtf.csrf import CSRFProtect, CSRFError
from helper.getbmedata import getBMEData1
from helper.lights import LightsTimeForm, lights_parse
import configparser
from datetime import datetime

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


@app.route("/index", methods=['GET', 'POST'])
@app.route("/")
def index():
    return render_template('index.html', title="Main page")


@app.route("/lights", methods=['GET', 'POST'])
def addtime():
    form = LightsTimeForm()
    config = configparser.ConfigParser()
    config.read('applicat/configs/time_config.ini')

    t1_start_now = config['LIGHTTIME_01']['START01']
    t1_stop_now = config['LIGHTTIME_01']['STOP01']

    if form.validate_on_submit():
        lights_parse()

        print(form.t1_start.data)
        flash("Time updated successfully!", "success")
        return redirect(request.url)
    return render_template('lights.html', title='Changing Light Schedule', form=form, koo=t1_start_now, poo=t1_stop_now)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
