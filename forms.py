from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

class NameEmailForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
    def validate_email(self, field):
        if 'utoronto' not in field.data.lower():
            raise ValidationError("Please include an '@' in the email address. 'utoronto' is missing an '@'.")