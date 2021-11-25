from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Student, Instrument, StudentInstrument
from . import db
import json
import sqlalchemy

views = Blueprint('views', __name__)


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

    # checkouts =  StudentInstrument.query.all().Join(Student)
    # checkouts = Student.query.join(Student.instruments)
    # checkouts = db.session.query(Student).join(Instrument,Student.instruments)
    # checkouts = db.session.query.join(Instrument)
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

# Checkouts
@views.route('/checkout', methods=['GET','POST'])
@login_required
def checkout_list():
    # checkouts = StudentInstrument.query.all()
    # students = Student.query.join(StudentInstrument).join(Instrument).all()
    students = Student.query(Student.id, Student.first_name).join(StudentInstrument).query(StudentInstrument.checkout_date).join(Instrument).query(Instrument.type).all()

    return render_template("checkout_list.html",students=students, user=current_user)    