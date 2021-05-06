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
    name = db.Column(db.String(200), index=True, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    score = db.relationship("Score", uselist=False, back_populates="prediction")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Prediction {}>'.format(self.name)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_1 = db.Column(db.String(200), index=True, unique=True)
    score_2 = db.Column(db.String(200), index=True, unique=True)
    prediction = db.relationship("Prediction", back_populates="score")

    def __repr__(self):
        return '<Prediction {}>'.format(self.name)