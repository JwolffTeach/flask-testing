from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, ZoneSchedule

class ZoneScheduleForm(FlaskForm):
    zone = IntegerField('Zone Number', validators=[DataRequired()])
    runLength = IntegerField('Length(Minutes)', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')


class EditZoneScheduleForm(FlaskForm):
    id = HiddenField("ID")
    zone = IntegerField('Zone Number', validators=[DataRequired()])
    runLength = IntegerField('Length(Minutes)', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

    def __init__(self, original_id, *args, **kwargs):
        super(EditZoneScheduleForm, self).__init__(*args, **kwargs)
        self.original_id = original_id
