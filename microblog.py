import RPi.GPIO as GPIO
import time
from app import create_app, db
from app.models import User, Post
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler

def show_zones():
    with app.app_context():
        from app.models import ZoneSchedule
        from app.models import Valve
        zonesNums = ZoneSchedule.query.all()
        valves = Valve.query.all()
        
        GPIO.setmode(GPIO.BCM)
        SleepTimeL = 0.5
        gpioPins = [2,3,4,17,27,22,10,9]
        for i in gpioPins:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
        
        try:
            for valve in valves:
                GPIO.output(valve.gpio_pin, GPIO.LOW)
                print(valve.valve, " ", valve.description, "is running.")
                time.sleep(SleepTimeL)
                GPIO.output(valve.gpio_pin, GPIO.HIGH)
                time.sleep(SleepTimeL)
            GPIO.cleanup()
            print ("Good bye!")

        except:
            print("  Quit")
            # Reset GPIO settings
            GPIO.cleanup()


        #runLengths = []
        #for zone in zones:
        #    runLengths.append(zone.RunLengths)
        #for valve in Valves:
        #    gpioPins.append(valve.gpio_pin)


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': show_zones,
            'trigger': 'cron',
            'replace_existing': True,
            'hour': '23',
            'minute': '03'
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    }

    SCHEDULER_API_ENABLED = True

app = create_app()
app.config.from_object(Config())

# Scheduler Stuff
sched = APScheduler()
sched.init_app(app)
sched.start()
scheduler = sched.scheduler

# You can reschedule it by doing this:
scheduler.reschedule_job('job1', trigger='cron', hour='23', minute='17')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}