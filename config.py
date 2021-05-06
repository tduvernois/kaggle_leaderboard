import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREDICTION_RESULT_PATH = '/Users/thomasduvernois/python/flask/hello_world/predictions'
    PREDICTION_RESULT_SOLUTION_PATH = '/Users/thomasduvernois/python/flask/hello_world/predictions/solutions.csv'



