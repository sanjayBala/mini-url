from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class MainForm(FlaskForm):
    original_url = StringField('Original URL', validators=[DataRequired(), Length(min=4, max=120)])
    submit = SubmitField('Encode!')