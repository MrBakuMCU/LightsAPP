# LightsAPP

To add a flask function to Cron:
1) In Flask:

@app.cli.command()
def random():
    """Run scheduled job."""
    print(str(datetime.utcnow()), 'Just a random job...')
    time.sleep(5)
    print(str(datetime.utcnow()), 'Done!')
    
2) In Cron:

* * * * * cd /usr/projects/03/server && export FLASK_APP=server.py && /usr/local/bin/flask random>>scheduled.log 2>&1

***************************************************************************

