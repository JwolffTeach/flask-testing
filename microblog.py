from app import create_app, db
from app.models import User, Post
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler


def show_zones():
    with app.app_context():
        from app.models import ZoneSchedule
        zones = ZoneSchedule.query.all()
        #for zone in zones:
        #    print(zone.runLength)

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': show_zones,
            'trigger': 'interval',
            'replace_existing': True,
            'seconds': 2
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    }

    SCHEDULER_API_ENABLED = True

app = create_app()
app.config.from_object(Config())
db.drop_all()
db.create_all()

# Scheduler Stuff
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}