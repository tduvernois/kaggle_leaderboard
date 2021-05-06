from app import app, db
from app.forms import TeamForm, UploadResultForm
from flask import render_template, flash, redirect, url_for
from app.models import Team, Member, Prediction
from werkzeug.utils import secure_filename
import os
from flask import request
import csv
from app import predictions_corrections
from datetime import datetime


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
        return redirect(url_for('index'))
    return render_template('register_team.html', title='Sign In', form=form)


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/prediction', methods=['GET', 'POST'])
def submit_prediction():
    form = UploadResultForm()
    if request.method == 'POST' and form.validate_on_submit():
        team_name = form.team_name.data
        team = Team.query.filter_by(name=team_name).first()
        if team is None:
            flash('The team does not exist')
        else:
            file_libertyUS = form.file_libertyUS.data
            file_libertySpain = form.file_libertySpain.data
            if allowed_file(file_libertyUS.filename) and allowed_file(file_libertySpain.filename):
                libertyUS_false_pred, libertyUS_true_pred = file_handler(file_libertyUS, team_name)
                libertySpain_false_pred, libertySpain_true_pred = file_handler(file_libertySpain, team_name)
                score_LibertyUs = libertyUS_true_pred / (libertyUS_true_pred + libertyUS_false_pred)
                score_LibertySpain = libertySpain_true_pred / (libertySpain_true_pred + libertySpain_false_pred)
                prediction = Prediction(
                    team_id=team.id,
                    file_name_LibertyUs=file_libertyUS.filename,
                    file_name_LibertySpain=file_libertySpain.filename,
                    score_LibertyUs=score_LibertyUs,
                    score_LibertySpain=score_LibertySpain
                )
                db.session.add(prediction)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('The file is not a csv')

    return render_template('submit_predictions.html', title='Submit predictions',
                           form=form)


def create_file_name(file_name, team_name):
    return f'{team_name}_{file_name}_{datetime.utcnow}'


def file_handler(file, team_name):
    filename_to_secure = create_file_name(file.filename, team_name)
    filename = secure_filename(filename_to_secure)
    # TODO: add arg to compare with client's dataset
    file_path = os.path.join(app.config['PREDICTION_RESULT_PATH'], filename)
    file.save(file_path)
    predictions = {}
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            predictions[row['id']] = row['status']
    counter_true_pred = 0
    counter_false_pred = 0
    for key, val in predictions_corrections.items():
        if predictions[key] == val:
            counter_true_pred = counter_true_pred + 1
        else:
            counter_false_pred = counter_false_pred + 1
    return counter_false_pred, counter_true_pred
