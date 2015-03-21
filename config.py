import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root:route91cap%@springboard-rds.corrsqtz0i3y.ap-southeast-1.rds.amazonaws.com/geekApp'
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')
