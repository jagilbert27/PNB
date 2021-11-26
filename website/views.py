from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Student, Instrument, StudentInstrument, InstrumentType
from . import db
import json
import sqlalchemy
import datetime

views = Blueprint('views', __name__)

@views.route('/Fill', methods=['GET', 'POST'])
@login_required
def fill():
    # Clear
    StudentInstrument.query.delete()
    Instrument.query.delete()
    Student.query.delete()
    InstrumentType.query.delete()
    db.session.commit()
    flash('DB Cleared')

    db.session.add(InstrumentType(name='Fiddle'))
    db.session.add(InstrumentType(name='Guitar'))
    db.session.commit()
    db.session.add(Instrument(type_id=1, tag='F1'))
    db.session.add(Instrument(type_id=2, tag='G1'))
    db.session.add(Student(email='a@a.com',first_name='Alpha',last_name='A'))
    db.session.add(Student(email='b@b.com',first_name='Bravo',last_name='B'))
    db.session.add(Student(email='c@c.com',first_name='Charlie',last_name='C'))
    db.session.commit()
    db.session.add(StudentInstrument(student_id=1, instrument_id=1, checkout_date=datetime.datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=1, instrument_id=2, checkout_date=datetime.datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=2, instrument_id=1, checkout_date=datetime.datetime(2021,11,1)))
    db.session.commit()
    flash('DB initialized with test data')
    return redirect(url_for('views.home'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# Student
@views.route('/student/new', methods=['GET','POST'])
@login_required
def student_new():
    if request.method == 'POST':
        try:
            student = Student(
                email = request.form.get('email'),
                first_name = request.form.get('firstName'),
                last_name = request.form.get('lastName')
                )
            db.session.add(student)
            db.session.commit()
            flash('Student Added!', category='success')
            return redirect(url_for('views.student',id=student.id, user=current_user))
        except sqlalchemy.exc.IntegrityError as ex:
            db.session.rollback()
            flash(f'Save Failed {type(ex)}', category='error')
    return render_template("student_edit.html",student=student, user=current_user)


@views.route('/student/<int:id>', methods=['GET','POST'])
@login_required
def student_edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("student_edit.html", student=student, user=current_user)

    student.email = request.form.get('email')
    student.first_name = request.form.get('first_name')
    student.last_name = request.form.get('last_name')
    db.session.commit()
    flash('Student Updated!', category='success')
    return redirect(url_for('views.student_edit',id=student.id, user=current_user))

@views.route('/instrument/new', methods=['GET','POST'])
@login_required
def instrument_new():
    instrument = Instrument()
    if request.method == 'POST':
        instrument.type = request.form['type']
        # instrument.size = request.form['size']
        instrument.brand = request.form.get('brand')
        db.session.add(instrument)
        db.session.commit()
        flash('Instrument Added!', category='success')
        return redirect(url_for('views.instrument',id=instrument.id, user=current_user))

    return render_template("instrument_new.html",user=current_user)    

@views.route('/instrument/<int:id>', methods=['GET','POST'])
@login_required
def instrument_edit(id):
    instrument = Instrument.query.get_or_404(id)
    return render_template("instrument_edit.html", instrument=instrument, user=current_user)

# Checkouts
@views.route('/checkout', methods=['GET','POST'])
@login_required
def checkout_list():
    # checkouts = StudentInstrument.query.all()
    # students = Student.query.join(StudentInstrument).join(Instrument).all()
    students = Student.query.all()

    msg = "Student structure:<br/><br/>"
    for student in students:
        msg += f'Student.first_name: {student.first_name} <br/>'
        for checkout in student.instruments:
            msg += f'    Checkout Date {checkout.checkout_date.strftime("%m/%d/%Y")} <br/>'
            msg += f'        Type: {checkout.instrument.type} <br/><br/>'
    # return msg

    return render_template("checkout_list.html",students=students, user=current_user)    