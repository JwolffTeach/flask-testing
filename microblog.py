import time
from app import create_app, db
from app.models import User, Post
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
import taskScheduler

class ScheduleConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': taskScheduler.dummy,
            'trigger': 'cron',
            'replace_existing': True,
            'hour': '00',
            'minute': '33',
            'second': '50'
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    }

    SCHEDULER_API_ENABLED = True

app = create_app()
app.config.from_object(ScheduleConfig())

with app.app_context():
    taskScheduler.start_sched()

#with app.app_context():
# Scheduler Stuff
#current_app.sched.start()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}