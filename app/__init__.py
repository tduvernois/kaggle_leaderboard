from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import csv


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

predictions_corrections = {}
with open(app.config['PREDICTION_RESULT_SOLUTION_PATH'], mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file,  delimiter=';')
    for row in csv_reader:
        predictions_corrections[row['id']] = row['status']

from app import routes, models

