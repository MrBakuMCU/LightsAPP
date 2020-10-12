from wtforms.fields.html5 import TimeField
from wtforms import SubmitField
from flask_wtf import FlaskForm
import configparser
from datetime import datetime, timedelta


class LightsTimeForm(FlaskForm):
    # Let's create form objects

    t1_start = TimeField('Start time:', format='%H:%M')
    t1_stop = TimeField('Stop time:', format='%H:%M')

    submit = SubmitField("Submit")


# This code would save the time selected in form to the INI file

def lights_parse():
    form = LightsTimeForm()
    t1_start = form.t1_start.data
    t1_stop = form.t1_stop.data

    t1_now = str(datetime.now())[:-7]
    t1_updatedon = datetime.strptime(t1_now, "%Y-%m-%d %H:%M:%S")
    tconfig = configparser.ConfigParser()

    time_data = {'LIGHTTIME_01': dict(START01=t1_start, STOP01=t1_stop, UPDATEDON=t1_updatedon)}
    tconfig.read_dict(time_data)

    tstart1 = tconfig['LIGHTTIME_01']['START01']
    tstop1 = tconfig['LIGHTTIME_01']['STOP01']
    timestamp1 = tconfig['LIGHTTIME_01']['UPDATEDON']

    # This just prints the time to the terminal for us to see that everything was recorded correctly (not necessary)

    print("START:", {tstart1})
    print('STOP:', {tstop1})
    print('UPDATED:', {timestamp1})

    with open('static/configs/time_config.ini', 'w') as configfile:
        tconfig.write(configfile)
