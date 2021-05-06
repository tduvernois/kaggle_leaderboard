from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FieldList, FormField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired


class TeamForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired()])
    team_member_1 = StringField('Team member', validators=[DataRequired()])
    team_member_2 = StringField('Team member')
    team_member_3 = StringField('Team member')
    team_member_4 = StringField('Team member')

    submit = SubmitField('Create Team')


class UploadResultForm(FlaskForm):

    file_libertyUS = FileField(validators=[FileRequired()])
    file_libertySpain = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')