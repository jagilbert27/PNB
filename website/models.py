from sqlalchemy.sql.expression import column
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Student(db.Model):
    __tablename__ = 'students'
    id= db.Column( db.Integer, primary_key=True)
    checkouts = relationship("StudentInstrument",back_populates="student")
    email =  db.Column( db.String(150), unique=True)
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

class InstrumentCondition(db.Model):
    __tablename__ = 'instrument_conditions'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='condition')
    name          = db.Column(db.String)

class InstrumentStatus(db.Model):
    __tablename__ = 'instrument_statuses'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='status')
    name          = db.Column(db.String)

class StudentInstrument(db.Model):
    __tablename__ = 'students_instruments'
    id            = db.Column(db.Integer, primary_key=True)
    student_id    = db.Column(db.ForeignKey('students.id'))
    instrument_id = db.Column(db.ForeignKey('instruments.id'))
    checkout_date = db.Column(db.Date)
    student=relationship("Student",back_populates="checkouts")
    instrument=relationship("Instrument",back_populates="checkouts")
    checkout_condition = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    return_condition = db.Column(db.Integer)
    return_location = db.Column(db.String(100))
    notes = db.Column(db.String(1000))
    __table_args__ = (UniqueConstraint('student_id', 'instrument_id', 'checkout_date', name='_unique_student_instrument_checkoutdate'),)    

 
