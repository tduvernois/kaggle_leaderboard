from app import db
from app.models import Team, Member

teams = Team.query.all()
print(teams)

team = Team.query.filter_by(name='ferfe').first()
print(team)

members = Member.query.all()
print(members)
