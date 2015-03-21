from app import db, app
import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


class MemberDetails(db.Model):
    __tablename__ = "member"
    __searchable__ = ['name', '']

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
