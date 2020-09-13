from re import match
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class MainForm(FlaskForm):
    original_url = StringField('Original URL', validators=[DataRequired(), Length(min=8, max=120)])
    submit = SubmitField('Submit')
    def validate_original_url(self, original_url):
        """
            Checks for http/https prefix
        """
        if not match('^http[s]{0,1}://', original_url.data):
            raise ValidationError('URL needs a https:// or http:// prefix.')