import time
import RPi.GPIO as GPIO
from flask import current_app
from app import create_app, db, sched
from app.models import User, Post, ZoneSchedule, Valve
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def start_sched():

    scheduler = sched.scheduler

    scheduler.add_job(show_zones, 'cron', hour='05', minute='48', replace_existing= True, args=[current_app._get_current_object()])

    scheduler.start()

def show_zones(app):
    with app.app_context():
        print("starting...")
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


def dummy():
    print("Yep.")