from app import app, db
from app.forms import TeamForm, UploadResultForm
from flask import render_template, flash, redirect, url_for
from app.models import Team, Member, Prediction, get_last_prediction
from werkzeug.utils import secure_filename
import os
from flask import request
import csv
from app import get_scores_from_file, scores_solution_Spain, scores_solution_US
from datetime import datetime
from flask import jsonify
from app.counter import Counter
import numpy as np
from sklearn.metrics import average_precision_score
from numpy import genfromtxt


@app.route('/')
@app.route('/overview')
def overview():
    return render_template('Overview.html', title='Overview')


@app.route('/register_team', methods=['GET', 'POST'])
def register_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(name=form.team_name.data).first()
        if team is not None:
            flash('This team already exists')
            return redirect(url_for('register_team'))

        members = [Member(name=form.team_member_1.data)]
        if form.team_member_2.data != '':
            members.append(Member(name=form.team_member_2.data))
        if form.team_member_3.data != '':
            members.append(Member(name=form.team_member_3.data))
        if form.team_member_4.data != '':
            members.append(Member(name=form.team_member_4.data))

        team = Team(name=form.team_name.data, members=members)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('overview'))
    return render_template('register_team.html', title='Sign In', form=form)


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/prediction', methods=['GET', 'POST'])
def submit_prediction():
    form = UploadResultForm()
    teams = [t.name for t in Team.query.all()]
    print(form.data)
    if request.method == 'POST' and request.form['team'] is not None and form.validate_on_submit():
        team_name = request.form['team']
        team = Team.query.filter_by(name=team_name).first()
        if team is None:
            flash('The team does not exist')
        else:
            if team.number_of_submissions_last_24hours() >= app.config['MAX_TEAM_SUBMISSIONS_PER_DAY']:
                flash('Max number of submissions in the past 24 hours hit')
            else:
                file_libertyUS = form.file_libertyUS.data
                file_libertySpain = form.file_libertySpain.data
                if allowed_file(file_libertyUS.filename) and allowed_file(file_libertySpain.filename):
                    score_LibertyUs = get_avg_precision_score_from_file(file_libertyUS, team_name, True)
                    score_LibertySpain = get_avg_precision_score_from_file(file_libertySpain, team_name)
                    prediction = Prediction(
                        team_id=team.id,
                        file_name_LibertyUs=file_libertyUS.filename,
                        file_name_LibertySpain=file_libertySpain.filename,
                        score_LibertyUs=score_LibertyUs,
                        score_LibertySpain=score_LibertySpain
                    )
                    db.session.add(prediction)
                    db.session.commit()
                    return redirect(url_for('leaderboard'))
                else:
                    flash('The file is not a csv')

    return render_template('submit_predictions.html', title='Submit predictions', teams=teams,
                           form=form)


def create_file_name(file_name, team_name):
    return f'{team_name}_{file_name}_{datetime.utcnow()}'


def save_file_and_return_path(file, team_name):
    filename_to_secure = create_file_name(file.filename, team_name)
    filename = secure_filename(filename_to_secure)
    # TODO: add arg to compare with client's dataset
    file_path = os.path.join(app.config['PREDICTION_RESULT_PATH'], filename)
    file.save(file_path)
    return file_path


def get_avg_precision_score_from_file(file, team_name, is_us_dataset=False):
    file_path = save_file_and_return_path(file, team_name)

    scores = get_scores_from_file(file_path)

    if is_us_dataset:
        score = average_precision_score(scores_solution_US, scores)
    else:
        score = average_precision_score(scores_solution_Spain, scores)
    return score


@app.route('/leaderboard')
def leaderboard():
    teams = Team.query.all()
    teams_with_best_prediction_and_best_score = {}
    for team in teams:
        best_team_prediction, best_team_score = team.get_team_best_prediction()
        if best_team_prediction is not None:
            teams_with_best_prediction_and_best_score[team.id] = {'prediction': best_team_prediction,
                                                                  'score': best_team_score,
                                                                  'team': team}
    teams_with_best_score_sorted = dict(sorted(teams_with_best_prediction_and_best_score.items(),
                                               key=lambda item: item[1]['score'],
                                               reverse=True))

    last_prediction = get_last_prediction()
    last_prediction_team_name = last_prediction[0].team.name
    last_prediction_timestamp = last_prediction[0].timestamp.strftime("%Y-%m-%d %H:%M")

    return render_template('leaderboard.html', title='Leaderboard',
                           teams_with_best_score_sorted=teams_with_best_score_sorted,
                           last_prediction_team_name=last_prediction_team_name,
                           last_prediction_timestamp=last_prediction_timestamp,
                           counter=Counter())


@app.route('/teams')
def teams():
    teams = [t.name for t in Team.query.all()]
    team_submissions = {}
    return render_template('teams.html', title='Teams', teams=teams, team_submissions=team_submissions)


@app.route('/team_submissions/<name>')
def team_submissions(name):
    team = Team.query.filter_by(name=name).first()
    submissions = team.get_team_submissions_all()

    submissions_json = []
    for s in submissions:
        s_json = {'score_libertyUs': s.score_LibertyUs,
                  'score_LibertySpain': s.score_LibertySpain,
                  'timestamp': s.timestamp
                  }
        submissions_json.append(s_json)
    return jsonify(submissions_json)

    return jsonify({'submissions': submissions})
