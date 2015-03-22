import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root:route91cap%@springboard-rds.corrsqtz0i3y.ap-southeast-1.rds.amazonaws.com/geekApp'
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '808299189209040',
        'secret': '7cb2d556c26cebd48062f36f7951e2d5'
    },
    'twitter': {
        'id': 'Zel5GJWtHMlTBm8jmLGZsGdeo',
        'secret': 'Inxc7UI4L0WMfhOauADQ6QZHT2TDziDvKr4Jkn7EWZjRuSATeb'
    },
    'linkedin': {
        'id': '78puisghrag04v',
        'secret': 'KOOpRWJdla9DMvKc'
    }
}