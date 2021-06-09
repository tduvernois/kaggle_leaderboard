import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREDICTION_RESULT_PATH = os.environ.get('APP_PATH') or '/Users/thomasduvernois/python/flask/hello_world/predictions'
    MAX_TEAM_SUBMISSIONS_PER_DAY = 100
    if os.environ.get('APP_PATH') is not None:
        PREDICTION_RESULT_SOLUTION_PATH = os.path.join(os.environ.get('APP_PATH'), 'solutions.csv')
    else:
        PREDICTION_RESULT_SOLUTION_PATH_US = '/Users/thomasduvernois/python/flask/hello_world/predictions/sol.csv'
        PREDICTION_RESULT_SOLUTION_PATH_SPAIN = '/Users/thomasduvernois/python/flask/hello_world/predictions/sol.csv'




