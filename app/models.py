from app import db
from helpers import generate_id


class MemberAttendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.String(255), primary_key=True)
    division_or_seat_no = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    Loksabha = db.Column(db.String(255), nullable=True)
    session = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    constituency = db.Column(db.String(255), nullable=False)
    total_sitting = db.Column(db.String(255), nullable=False)
    no_days_member_signed_the_register = db.Column(db.String(255),
                                                   nullable=False)
    errors = {}

    def __init__(self, **kwargs):
        """Initialize the MemberAttendance object based on the method"""

        def __init__(self, **kwargs):
            self.id = generate_id()
            for key, value in kwargs.iteritems():
                try:
                    setattr(self, key, value)
                except:
                    # Returns a dictionary of empty field errors
                    MemberAttendance.errors[key] = "EMPTY FIELD"
