import time
from datetime import datetime
import calendar
import os
import RPi.GPIO as GPIO
from flask import current_app, render_template
from app import create_app, db, sched
from app.models import User, Post, ZoneSchedule, Valve
from app.email import send_email
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def start_sched():

    scheduler = sched.scheduler
    scheduler.add_job(run_sprinklers, 'cron', id='sprinklerjob', hour='03', minute='30', replace_existing= True, args=[current_app._get_current_object()])
    #jobid = scheduler.
    scheduler.start()
    modify_starttime('sprinklerjob', '03', '30')

def writeLog(text):
    logFile = open('/home/pi/myproject/logs/taskscheduler.log', 'a')
    logFile.write(text+'\n')
    logFile.close()

def run_sprinklers(app):

    os.environ["SPRINKLERS_STATUS"] = "READY"
    with app.app_context():
        logFile = open('/home/pi/myproject/logs/taskscheduler.log', 'a')
        writeLog(str(datetime.now())+': Sprinklers are starting.')
        print("starting...")
        zonesNums = ZoneSchedule.query.all()
        valves = Valve.query.all()
        
        # This query gives us the scheduled zones:
        # id, valve, gpio_pin, and runLength
        scheduledZones = ZoneSchedule.query.join(Valve, ZoneSchedule.zone == Valve.valve).add_columns(Valve.valve, Valve.description, Valve.gpio_pin, ZoneSchedule.runLength, ZoneSchedule.m, ZoneSchedule.t, ZoneSchedule.w, ZoneSchedule.th, ZoneSchedule.f, ZoneSchedule.s, ZoneSchedule.su)
        currentDay = calendar.day_name[datetime.now().weekday()] # GIves Monday, Tuesday, Wednesday, etc.
        GPIO.setmode(GPIO.BCM)

        # Prepare all valves
        for valve in valves:
            GPIO.setup(valve.gpio_pin, GPIO.OUT)
            GPIO.output(valve.gpio_pin, GPIO.HIGH)
            writeLog(str(datetime.now())+': Valves are reset.')
        
        try:
            for zone in scheduledZones:
                if((currentDay=="Monday" and zone.m)
                or (currentDay=="Tuesday" and zone.t)
                or (currentDay=="Wednesday" and zone.w)
                or (currentDay=="Thursday" and zone.th)
                or (currentDay=="Friday" and zone.f)
                or (currentDay=="Saturday" and zone.s)
                or (currentDay=="Sunday" and zone.su)
                ):

                    if(os.environ["SPRINKLERS_STATUS"] == "READY"):
                        running = True
                        progressSec = 0
                        progressPercent = 0.0
                        zoneRunLength = zone.runLength * 60 # Num Seconds this Zone will run
                        GPIO.output(zone.gpio_pin, GPIO.LOW)
                        writeLog(str(datetime.now())+': '+str(zone.valve)+ " "+ zone.description+ " is running on GPIO pin "+ str(zone.gpio_pin)+ " for "+ str(zone.runLength) + " minutes.")
                        while running: # Every minute, check if sprinkler status is set to ready.
                            if(os.environ["SPRINKLERS_STATUS"] == "READY" and progressSec < zoneRunLength):
                                time.sleep(10) # Sleep for 10 seconds.
                                progressSec += 10
                                progressPercent = progressSec/zoneRunLength
                                print(str(datetime.now())+': '+str(zone.valve)+ " "+ zone.description+': '+"Current Progress: "+"{:.2%}".format(progressPercent))
                                writeLog(str(datetime.now())+': '+str(zone.valve)+ " "+ zone.description+": Current Progress: "+"{:.2%}".format(progressPercent))
                            else:
                                running = False
                                progressSec = 0
                        GPIO.output(zone.gpio_pin, GPIO.HIGH)
                        writeLog(str(datetime.now())+': '+str(zone.valve)+' is off.')
                        time.sleep(5)
                    else:
                        #app.logger.info('SPRINKLER_STATUS: ', current_app.config['SPRINKLERS_STATUS'])
                        break
                GPIO.cleanup()
                writeLog(str(datetime.now())+': '+'Cleaning Up!')

        except:
            print("  Quit")
            # Reset GPIO settings
            GPIO.cleanup()
        writeLog(str(datetime.now())+': '+'Sprinklers are done.')

def stop_all_sprinklers(app):
    with app.app_context():
        scheduler = sched.scheduler        
        for job in sched.scheduler.get_jobs():
            job = sched.scheduler.get_job(job.id)
            #sched.scheduler.pause_job(job.id)
        print("Stopping all sprinklers.")
        GPIO.setmode(GPIO.BCM)
        valves = Valve.query.all()
        for valve in valves:
            print("reseting valves...")
            GPIO.setup(valve.gpio_pin, GPIO.OUT)
            GPIO.output(valve.gpio_pin, GPIO.HIGH)
        print("Cleaning up.")
        # Reset GPIO settings
        GPIO.cleanup()
        os.environ["SPRINKLERS_STATUS"] = "STOP"
        time.sleep(1)
        #current_app.config['SPRINKLERS_STATUS'] = "READY"
        



def modify_starttime(jobid, startHour, startMinute):
    scheduler = sched.scheduler
    scheduler.reschedule_job(jobid, trigger='cron', hour=startHour, minute=startMinute)
