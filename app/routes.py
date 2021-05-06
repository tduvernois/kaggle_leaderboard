from app import app, db
from flask import render_template, request
from app.forms import TeamForm, UploadResultForm
from flask import render_template, flash, redirect, url_for
from app.models import Team, Member, Prediction
from werkzeug.utils import secure_filename
import os


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/register_team', methods=['GET', 'POST'])
def register_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(name=form.team_name.data).first()
        if team is not None:
            print('This team already exists')
            return redirect(url_for('register_team'))

        members = []
        members.append(Member(name=form.team_member_1.data))
        members.append(Member(name=form.team_member_2.data))
        members.append(Member(name=form.team_member_3.data))
        members.append(Member(name=form.team_member_4.data))

        team = Team(name=form.team_name.data, members=members)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('register_team'))
    return render_template('register_team.html', title='Sign In', form=form)


@app.route('/prediction', methods=['GET', 'POST'])
def submit_prediction():
    form = UploadResultForm()
    print(form.file.data)
    if request.method == 'POST' and form.validate_on_submit():

        f = form.file.data
        filename = secure_filename(f.filename)
        team = form.team_name.data
        filename_saved = team + '-' + filename
        f.save(os.path.join(
            app.config['PREDICTION_RESULT_PATH'], filename_saved
        ))
        # Prediction(name=filename_saved)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('submit_predictions.html', title='Submit predictions',
                           form=form)