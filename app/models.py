from app import db
from datetime import datetime


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    members = db.relationship('Member', backref='team', lazy=True)
    predictions = db.relationship('Prediction', backref='team', lazy=True)

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Member {}>'.format(self.name)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    file_name_LibertyUs = db.Column(db.String(200), index=True, unique=True)
    file_name_LibertySpain = db.Column(db.String(200), index=True, unique=True)
    score_LibertyUs = db.Column(db.Float(10), index=True, unique=True)
    score_LibertySpain = db.Column(db.Float(10), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Prediction {}>'.format(self.name)