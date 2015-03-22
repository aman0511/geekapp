from app import db, app
import sys
from flask.ext.login import UserMixin
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


class MemberDetails(db.Model):
    __tablename__ = "member"
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    division_or_seat_no = db.Column(db.String(255), nullable=True)
    Loksabha = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=False)
    constituency = db.Column(db.String(255), nullable=False)
    sessions = db.relationship('memberSession',
                               backref=db.backref('MemberDetails',
                                                  lazy='joined'),
                               lazy='dynamic')
    total_avg = db.Column(db.String(255), nullable=True)
    errors = {}

    def __init__(self, **kwargs):
        """Initialize the MemberAttendance object based on the method"""
        for key, value in kwargs.iteritems():
            try:
                setattr(self, key, value)
            except:
                # Returns a dictionary of empty field errors
                MemberDetails.errors[key] = "EMPTY FIELD"

    @staticmethod
    def get_member(id):
        return db.session.query(MemberDetails).filter_by(
                    id=id).first()
if enable_search:
    whooshalchemy.whoosh_index(app, MemberDetails)


class memberSession(db.Model):
    """docstring for session"""
    __tablename__ = "membersession"
    id = db.Column(db.Integer, primary_key=True)
    Loksabha_session = db.Column(db.String(255), nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    total_sitting = db.Column(db.String(255))
    session_avg = db.Column(db.String(255), nullable=True)
    no_days_member_signed_the_register = db.Column(db.String(255))
    errors = {}

    def __init__(self, **kwargs):
        member = MemberDetails.get_member(int(kwargs['id']))
        kwargs.pop('id')
        self.MemberDetails = member
        for key, value in kwargs.iteritems():
            try:
                setattr(self, key, value)
            except:
                MemberDetails.errors = "empty field"


class User(db.Model, UserMixin):
    ''' User Table containing all primary data  '''

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    social_id = db.Column(db.String(255), nullable=True, unique=True)
    email = db.Column(db.String(255), index=True, nullable=False)
    errors = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            try:
                setattr(self, key, value)
            except:
                # Returns a dictionary of empty field errors
                User.errors[key] = "empty Field"

    @staticmethod
    def get_user(token=None):
        """returns user object for a specific user"""
        if token:
            return db.session.query(User).filter_by(
                social_id=token).first()

    @staticmethod
    def authenticate_user(**kwargs):
        """ authenticates a user and also enforces validations"""
        if kwargs['social_id']:
            user = User.get_user(token=kwargs['social_id'])
            if user:
                return user
            return
        else:
            User.errors['social_id'] = "AUTHENTICATION_FAIL"
            return
