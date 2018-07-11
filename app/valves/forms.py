from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

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