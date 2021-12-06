from os import name
from sqlalchemy.sql.expression import column
from . import db
from flask_user import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from datetime import datetime, timedelta 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')    
    email_confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='user_roles')
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    users = db.relationship('User', secondary='user_roles')
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))    

class Student(db.Model):
    __tablename__ = 'students'
    id= db.Column( db.Integer, primary_key=True)
    checkouts = relationship("StudentInstrument",back_populates="student")
    email =  db.Column( db.String(150))
    first_name =  db.Column( db.String(150))
    last_name =  db.Column( db.String(150))
    notes =  db.Column( db.String(150))
    birthday = db.Column( db.Date)

class Instrument(db.Model):
    __tablename__ = 'instruments'
    id            = db.Column(db.Integer, primary_key=True)
    type_id       = db.Column(db.Integer, db.ForeignKey('instrument_types.id'))
    size_id       = db.Column(db.Integer, db.ForeignKey('instrument_sizes.id'))
    status_id     = db.Column(db.Integer, db.ForeignKey('instrument_statuses.id'))
    condition_id  = db.Column(db.Integer, db.ForeignKey('instrument_conditions.id'))
    type          = relationship("InstrumentType", back_populates="instruments")
    size          = relationship("InstrumentSize",back_populates="instruments")
    condition     = relationship("InstrumentCondition",back_populates="instruments")
    status        = relationship("InstrumentStatus",back_populates="instruments")
    checkouts     = relationship("StudentInstrument",back_populates="instrument")
    tag           = db.Column(db.String(150))
    serial        = db.Column(db.String(150))
    brand         = db.Column(db.String(150))
    model         = db.Column(db.String(150))
    location      = db.Column(db.String(150))
    est_value     = db.Column(db.Integer)

class InstrumentType(db.Model):
    __tablename__ = 'instrument_types'
    id            = db.Column(db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='type')
    name          = db.Column(db.String(20))

class InstrumentSize(db.Model):
    __tablename__ = 'instrument_sizes'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='size')
    name          = db.Column(db.String)

class InstrumentStatus(db.Model):
    __tablename__ = 'instrument_statuses'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='status')
    name          = db.Column(db.String)

class StudentInstrument(db.Model):
    __tablename__           = 'students_instruments'
    __table_args__          = (UniqueConstraint('student_id', 'instrument_id', 'checkout_date', name='_unique_student_instrument_checkoutdate'),)    
    id                      = db.Column(db.Integer, primary_key=True)
    student_id              = db.Column(db.ForeignKey('students.id'))
    instrument_id           = db.Column(db.ForeignKey('instruments.id'))
    checkout_condition_id   = db.Column(db.Integer, db.ForeignKey('instrument_conditions.id'))
    return_condition_id     = db.Column(db.Integer, db.ForeignKey('instrument_conditions.id'))
    student                 = relationship("Student",back_populates="checkouts")
    instrument              = relationship("Instrument",back_populates="checkouts")
    checkout_condition      = relationship("InstrumentCondition", foreign_keys=[checkout_condition_id])
    return_condition        = relationship("InstrumentCondition", foreign_keys=[return_condition_id])
    checkout_date           = db.Column(db.Date)
    due_date                = db.Column(db.Date)
    return_date             = db.Column(db.Date)
    return_location         = db.Column(db.String(100))
    notes                   = db.Column(db.String(1000))

    @classmethod
    def from_request(cls, request):
        return cls

    # def __init__(self, request):
    #     try:
    #         self.checkout_date = datetime.strptime(request.form['checkout_date'],'%Y-%m-%d')
    #     except: pass
    #     try:
    #         self.due_date = datetime.strptime(request.form['due_date'],'%Y-%m-%d')
    #     except: pass
    #     try:
    #         self.return_date = datetime.strptime(request.form['return_date'],'%Y-%m-%d')
    #     except: pass
    #     self.student_id = request.form.get('student_id')
    #     self.instrument_id = request.form.get('instrument_id')
    #     self.checkout_condition_id = request.form.get('checkout_condition')
    #     self.return_condition_id = request.form.get('return_condition')
    #     self.return_location = request.form.get('return_location')
    #     self.notes = request.form.get('notes')


class InstrumentCondition(db.Model):
    __tablename__ = 'instrument_conditions'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='condition')
    name          = db.Column(db.String)

class Semester(db.Model):
    __tablename__ = 'semesters'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String)
    first_class_date = db.Column(db.Date)
    last_class_date  = db.Column(db.Date)
    earliest_checkout_date = db.Column(db.Date)
    latest_due_date = db.Column(db.Date)


    # @classmethod
    # def get_for_date(cls, **kw):
    #     obj = cls(**kw)
    #     db.session.add(obj)
    #     db.session.commit()

    # def for_date(cls, date):
    #     return Session.query(Users).filter(Users.id==userid).first()



