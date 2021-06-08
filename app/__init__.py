from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from numpy import genfromtxt

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


def get_scores_from_file(file_path):
    scores = genfromtxt(file_path)
    return scores


scores_solution = get_scores_from_file(app.config['PREDICTION_RESULT_SOLUTION_PATH'])

from app import routes, models
