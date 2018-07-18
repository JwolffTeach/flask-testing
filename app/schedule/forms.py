from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField, HiddenField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, ZoneSchedule

class ZoneScheduleForm(FlaskForm):
    zone = IntegerField('Zone Number', validators=[DataRequired()])
    runLength = IntegerField('Length(Minutes)', validators=[DataRequired()])
    m = BooleanField('Monday')
    t = BooleanField('Tuesday')
    w = BooleanField('Wednesday')
    th = BooleanField('Thursday')
    f = BooleanField('Friday')
    s = BooleanField('Saturday')
    su = BooleanField('Sunday')
    submit = SubmitField('Submit Changes')


class EditZoneScheduleForm(FlaskForm):
    id = HiddenField("ID")
    zone = IntegerField('Zone Number', validators=[DataRequired()], render_kw={'readonly': True})
    description = StringField('Description', render_kw={'readonly': True})
    runLength = IntegerField('Length(Minutes)', validators=[DataRequired()])
    m = BooleanField('Monday')
    t = BooleanField('Tuesday')
    w = BooleanField('Wednesday')
    th = BooleanField('Thursday')
    f = BooleanField('Friday')
    s = BooleanField('Saturday')
    su = BooleanField('Sunday')
    submit = SubmitField('Submit Changes')

    def __init__(self, original_id, *args, **kwargs):
        super(EditZoneScheduleForm, self).__init__(*args, **kwargs)
        self.original_id = original_id

class Schedule_Days_Form(FlaskForm):    
    theDays = [
        ('monday', 'M'), 
        ('tuesday', 'T'), 
        ('wednesday', 'W'),
        ('thursday', 'Th'), 
        ('friday', 'F'), 
        ('saturday', 'S'),
        ('sunday', 'Su')
        ]
    Days = SelectMultipleField(
        'Days', 
        choices=theDays, 
        option_widget=widgets.CheckboxInput(), 
        widget = widgets.ListWidget(prefix_label=False)
    )

class Schedule_Valves_Form(FlaskForm):
    monday = BooleanField()
    tuesday = BooleanField()
    wednesday = BooleanField()
    thursday = BooleanField()
    friday = BooleanField()
    saturday = BooleanField()
    sunday = BooleanField()
    selectall = BooleanField('selectAll')
    submit = SubmitField('Submit Changes')