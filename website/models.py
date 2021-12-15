from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
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
    external_id = db.Column(db.Integer)
    checkouts = relationship("StudentInstrument",back_populates="student")
    semesters = relationship("StudentSemester",back_populates="student")
    guardians = relationship("StudentGuardian",back_populates="student")
    email =  db.Column( db.String(150))
    first_name =  db.Column( db.String(150))
    last_name =  db.Column( db.String(150))
    notes =  db.Column( db.String(150))
    birthday = db.Column( db.Date)
    address = db.Column( db.String(150))
    phone = db.Column( db.String(20))

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

class InstrumentCondition(db.Model):
    __tablename__ = 'instrument_conditions'
    id            = db.Column( db.Integer, primary_key=True)
    instruments   = relationship(Instrument, back_populates='condition')
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

class Semester(db.Model):
    __tablename__    = 'semesters'
    id               = db.Column(db.Integer, primary_key=True)
    students         = relationship("StudentSemester",back_populates="semester") 
    name             = db.Column(db.String)
    start_date       = db.Column(db.Date)
    end_date         = db.Column(db.Date)
    first_class_date = db.Column(db.Date)
    last_class_date  = db.Column(db.Date)
    first_checkout_date = db.Column(db.Date)
    last_due_date  = db.Column(db.Date)

class StudentSemester(db.Model):
    __tablename__      = 'student_semester'
    id                 = db.Column( db.Integer, primary_key=True)
    student_id         = db.Column(db.ForeignKey('students.id'))
    semester_id        = db.Column(db.ForeignKey('semesters.id'))
    campus_id          = db.Column(db.ForeignKey('campuses.id'))
    student            = relationship("Student",back_populates="semesters")
    semester           = relationship("Semester",back_populates="students")
    campus             = relationship("Campus")
    signup_date        = db.Column( db.Date)
    grade              = db.Column( db.Integer)
    shirt_size         = db.Column( db.String(150))
    behavior_agreement = db.Column( db.Boolean)
    photo_permission   = db.Column( db.Boolean)
    hardship_requested = db.Column( db.Boolean)
    tuition_changed    = db.Column( db.Numeric(8,2))
    rental_charged     = db.Column( db.Numeric(8,2))
    total_paid         = db.Column( db.Numeric(8,2))
    paid_date          = db.Column( db.Date)

class Person(db.Model):
    __tablename__ = 'persons'
    id            = db.Column( db.Integer, primary_key=True)
    students      = relationship("StudentGuardian",back_populates="guardian")
    name          = db.Column( db.String(150))
    roles         = relationship("PersonsRoles",back_populates="person")

class PersonRole(db.Model):
    __tablename__ = 'person_role'
    id          = db.Column( db.Integer, primary_key=True)
    name        = db.Column( db.String(150))  # Parent, Teacher, Administrator, Patron, Follower
    persons     = relationship("PersonsRoles",back_populates="role")

class PersonsRoles(db.Model):
    __tablename__ = 'persons_roles'
    id            = db.Column( db.Integer, primary_key=True)
    person_id     = db.Column(db.ForeignKey('persons.id'))
    role_id       = db.Column(db.ForeignKey('person_role.id'))
    person        = relationship("Person",back_populates="roles")
    role          = relationship("PersonRole",back_populates="persons")

class GuardianType(db.Model):
    __tablename__   = 'guardian_types'
    id              = db.Column( db.Integer, primary_key=True)
    dependent_name  = db.Column( db.String(150)) #child, nephew, niece, grandchild
    guardian_name   = db.Column( db.String(150)) #mother, father, uncle, aunt...

class StudentGuardian(db.Model):
    __tablename__    = 'students_guardians'
    __table_args__    = (UniqueConstraint('student_id', 'guardian_id', name='_unique_student_guardian'),)    
    id               = db.Column( db.Integer, primary_key=True)
    student_id       = db.Column(db.ForeignKey('students.id'))
    guardian_id      = db.Column(db.ForeignKey('persons.id'))
    guardian_type_id = db.Column(db.ForeignKey('guardian_types.id'))
    student          = relationship("Student",back_populates="guardians")
    guardian         = relationship("Person", back_populates="students")
    guardian_type    = relationship("GuardianType")

class Campus(db.Model):
    __tablename__   = 'campuses'
    id              = db.Column( db.Integer, primary_key=True)
    name            = db.Column( db.String(150))

