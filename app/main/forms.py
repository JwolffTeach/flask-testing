from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, ZoneSchedule


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ValveForm(FlaskForm):
    valve = TextAreaField('Valve Number', validators=[DataRequired(), Length(min=1, max=2)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=140)])
    gpio_pin = TextAreaField('GPIO Pin', validators=[DataRequired(), Length(min=1, max=2)])
    submit = SubmitField('Add New Valve')

class EditValveForm(FlaskForm):
    id = TextAreaField('Valve Number', validators=[DataRequired(), Length(min=1, max=2)])
    valve = TextAreaField('Valve Number', validators=[DataRequired(), Length(min=1, max=2)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=140)])
    gpio_pin = TextAreaField('GPIO Pin', validators=[DataRequired(), Length(min=1, max=2)])
    submit = SubmitField('Submit Changes')

    def __init__(self, original_id, *args, **kwargs):
        super(EditValveForm, self).__init__(*args, **kwargs)
        self.original_id = original_id

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
