import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'ads.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_PATH = 'ads.db'
# DB_PATH = '/home/jurassic987/ads-api/ads.db'
