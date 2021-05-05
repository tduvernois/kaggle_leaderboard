from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    members = db.relationship('Member', backref='team', lazy=True)

    def __repr__(self):
        return '<Team {}>'.format(self.name)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Member {}>'.format(self.name)