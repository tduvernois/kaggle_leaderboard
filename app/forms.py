from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired
from app.models import Member


class TeamForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired()])
    submit = SubmitField('Create Team')