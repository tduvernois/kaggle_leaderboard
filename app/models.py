from app import db
from datetime import datetime


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    members = db.relationship('Member', backref='team', lazy=True)
    predictions = db.relationship('Prediction', backref='team', lazy=True)

    def __repr__(self):
        return '<Team {}>'.format(self.name)

    def get_team_best_prediction(self):
        predictions = self.predictions
        best_score = 0
        best_prediction = None
        for prediction in predictions:
            score = prediction.score_LibertySpain + prediction.score_LibertyUs
            if score > best_score:
                best_score = score
                best_prediction = prediction
        return best_prediction, best_score


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Member {}>'.format(self.name)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), index=True)
    file_name_LibertyUs = db.Column(db.String(200))
    file_name_LibertySpain = db.Column(db.String(200))
    score_LibertyUs = db.Column(db.Float(10))
    score_LibertySpain = db.Column(db.Float(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Prediction {}>'.format(self.name)

