from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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
    instruments = relationship("StudentInstrument",back_populates="student")
    email =  db.Column( db.String(150), unique=True)
    first_name =  db.Column( db.String(150))
    last_name =  db.Column( db.String(150))
    notes =  db.Column( db.String(150))
    birthday = db.Column( db.Date)


class Instrument(db.Model):
    __tablename__ = 'instruments'
    id       = db.Column(db.Integer, primary_key=True)
    students = relationship("StudentInstrument",back_populates="instrument")
    tag      = db.Column(db.String(150))
    serial   = db.Column(db.String(150))
    type     = db.Column(db.String(150))
    size     = db.Column(db.String(150))
    brand    = db.Column(db.String(150))

class StudentInstrument(db.Model):
    __tablename__ = 'students_instruments'
    student_id = db.Column(db.ForeignKey('students.id'),primary_key=True)
    instrument_id = db.Column(db.ForeignKey('instruments.id'),primary_key=True)
    student=relationship("Student",back_populates="instruments")
    instrument=relationship("Instrument",back_populates="students")
    checkout_date = db.Column(db.Date,primary_key=True)
    checkout_condition = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    return_condition = db.Column(db.Integer)
    return_location = db.Column(db.String(100))
    notes = db.Column(db.String(1000))
 