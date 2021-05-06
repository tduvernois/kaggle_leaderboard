from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FieldList, FormField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired

filenames = ['efz', 'fefezfefefz']

class TeamForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired()])
    team_member_1 = StringField('Team member', validators=[DataRequired()])
    team_member_2 = StringField('Team member', validators=[DataRequired()])
    team_member_3 = StringField('Team member', validators=[DataRequired()])
    team_member_4 = StringField('Team member', validators=[DataRequired()])

    submit = SubmitField('Create Team')



class UploadResultForm(FlaskForm):
    # team_name = SelectField('Username', validators=[DataRequired()], choices=filenames)
    team_name = StringField('Team name', validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')