from operator import or_
from re import X
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_user import current_user, login_required, roles_required, UserMixin
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import desc, null, select, text, true
from sqlalchemy.orm import load_only

from .models import Note, Student, Instrument, StudentInstrument, InstrumentType, InstrumentSize, InstrumentCondition, InstrumentStatus, Role, UserRoles, Semester
from . import db
import json
import sqlalchemy
from datetime import datetime, timedelta 

views = Blueprint('views', __name__)

@views.route('/Fill', methods=['GET', 'POST'])
@roles_required('dev')
@login_required
def fill():
    StudentInstrument.query.delete()
    Instrument.query.delete()
    Student.query.delete()
    InstrumentCondition.query.delete()
    InstrumentSize.query.delete()
    InstrumentType.query.delete()
    InstrumentStatus.query.delete()
    db.session.commit()
    flash('DB Cleared')

    db.session.add(InstrumentSize(id=1, name="Standard"))
    db.session.add(InstrumentSize(id=2, name="3/4"))
    db.session.add(InstrumentSize(id=3, name="1/2"))

    db.session.add(InstrumentType(id=1, name='Fiddle'))
    db.session.add(InstrumentType(id=2, name='Guitar'))
    db.session.add(InstrumentType(id=3, name='Mandolin'))
    db.session.add(InstrumentType(id=4, name='Banjo'))
    db.session.add(InstrumentType(id=5, name='Bass'))
    db.session.add(InstrumentType(id=6, name='Ukulele'))
    
    db.session.add(InstrumentCondition(id=5, name='New'))
    db.session.add(InstrumentCondition(id=4, name='Good'))
    db.session.add(InstrumentCondition(id=3, name='Fair'))
    db.session.add(InstrumentCondition(id=2, name='Poor'))
    db.session.add(InstrumentCondition(id=1, name='Broken'))

    db.session.add(InstrumentStatus(id=1, name='Available for checkout'))
    db.session.add(InstrumentStatus(id=2, name='Checked out to Student'))
    db.session.add(InstrumentStatus(id=3, name='Needs Repair'))
    db.session.add(InstrumentStatus(id=4, name='Out for Repair'))
    db.session.add(InstrumentStatus(id=5, name='Decommissioned'))

    db.session.add(Instrument(type_id=1, tag='F1', condition_id=3, status_id=1 ))
    db.session.add(Instrument(type_id=2, tag='G1', condition_id=4 ))

    db.session.add(Student(email='a@a.com',first_name='Alpha',last_name='A'))
    db.session.add(Student(email='b@b.com',first_name='Bravo',last_name='B'))
    db.session.add(Student(email='c@c.com',first_name='Charlie',last_name='C'))

    db.session.add(StudentInstrument(student_id=1, instrument_id=1, checkout_date=datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=1, instrument_id=2, checkout_date=datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=2, instrument_id=1, checkout_date=datetime(2021,11,1)))

    db.session.add(Semester(name='Winter 2021/2022', earliest_checkout_date = datetime(2021,10,1), latest_due_date = datetime(2022,2,1)))
    db.session.add(Semester(name='Spring 2022',      earliest_checkout_date = datetime(2022,2,2), latest_due_date = datetime(2022,6,1)))
    db.session.add(Semester(name='Summer 2022', earliest_checkout_date = datetime(2022,6,2), latest_due_date = datetime(2022,10,2)))

    # db.session.add(Role(id=1, name='dev'))
    # db.session.add(UserRoles( user_id=1, role_id=1))

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


# Student List
@views.route('/students', methods=['GET','POST'])
@login_required
def student_list():
    if request.method == 'GET':
        students = Student.query.all()
        return render_template("student_list.html", students=students, user=current_user)
    
    student_id=request.form['student-id-to-delete']
    student = Student.query.get(student_id)
    msg = f'Deleted Student {student.first_name} {student.last_name}'
    db.session.delete(student)
    db.session.commit()
    flash(msg, category='warning')
    return redirect(url_for('views.student_list'))

#Populate a student object from a request
def student_gather(student,request):
    student.email = request.form.get('email')
    student.first_name = request.form.get('first_name')
    student.last_name = request.form.get('last_name')

# Student New
@views.route('/student/new', methods=['GET','POST'])
@login_required
def student_new():
    if request.method == 'GET':
        return render_template("student_edit.html", student=Student(), user=current_user)

    # Delete Student
    # ToDo: see if I can post the form to /student/delete/id instead of here
    student = Student()
    db.session.add(student)
    student_gather(student,request)
    db.session.commit()
    flash(f'Added Student {student.first_name} {student.last_name}', category='success')
    return redirect(url_for('views.student_list'))


# Student Edit
@views.route('/student/edit/<int:id>', methods=['GET','POST'])
@login_required
def student_edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("student_edit.html", student=student, user=current_user)
    
    student_gather(student, request)
    flash(f'Updated Student {student.first_name} {student.last_name}', category='success')
    return redirect(url_for('views.student_list'))


# Student View
@views.route('/student/view/<int:id>', methods=['GET'])
@login_required
def student_view(id):
    student = Student.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("student_edit.html", student=student, user=current_user, readonly=True)


# Student Delete
@views.route('/delete-student', methods=['POST'])
def student_delete():
    request_data = json.loads(request.data)
    student_id = request_data['student_id']
    student= Student.query.get(student_id)
    msg = f'Deleted Student {student.first_name} {student.last_name}'
    if student:
        try:
            db.session.delete(student)
            db.session.commit()
            flash(msg, category='warning')
        except BaseException as ex:
            db.session.rollback()
            flash(f'Delete Failed {type(ex)}', category='error')
    return jsonify({})


# Instrument List
@views.route('/instruments', methods=['GET'])
@login_required
def instrument_list():
    instruments = Instrument.query.all()
    return render_template("instrument_list.html", instruments=instruments, user=current_user)


# Instrument New
@views.route('/instrument/new', methods=['GET','POST'])
@login_required
def instrument_new():
    instrument = Instrument()
    if request.method == 'POST':
        # instrument.type_id = request.form['instrument_type']
        instrument.size_id = request.form.get('size_id')
        instrument.brand = request.form.get('brand')
        db.session.add(instrument)
        db.session.commit()
        flash('Instrument Added!', category='success')
        return redirect(url_for('views.home'))
    
    instrument_types = InstrumentType.query.all()
    instrument_conditions = InstrumentCondition.query.all()
    instrument_sizes = InstrumentSize.query.all()
    instrument_statuses = InstrumentStatus.query.all()



    return render_template(
        "instrument_edit.html", 
        instrument=instrument, 
        instrument_types = instrument_types, 
        instrument_conditions=instrument_conditions,
        instrument_sizes = instrument_sizes,
        instrument_statuses = instrument_statuses,
        user=current_user) 


# Instrument Edit
@views.route('/instrument/edit/<int:id>', methods=['GET','POST'])
@login_required
def instrument_edit(id):
    instrument = Instrument.query.get_or_404(id)
    if request.method == 'POST':
        instrument.tag = request.form.get('instrument_tag')
        instrument.type_id = request.form.get('instrument_type')
        instrument.size_id = request.form.get('instrument_size')
        instrument.status_id = request.form.get('instrument_status')
        instrument.serial = request.form.get('instrument_serial')
        instrument.brand = request.form.get('instrument_brand')
        instrument.model = request.form.get('instrument_brand')
        instrument.condition_id = request.form.get('instrument_condition')
        instrument.location = request.form.get('instrument_location')
        instrument.est_value = request.form.get('instrument_value')
        db.session.add(instrument)
        db.session.commit()
        flash('Instrument Added!', category='success')
        return redirect(url_for('views.instrument_list'))
    instrument_types = InstrumentType.query.all()
    instrument_conditions = InstrumentCondition.query.all()
    instrument_sizes = InstrumentSize.query.all()
    instrument_statuses = InstrumentStatus.query.all()
    return render_template(
        "instrument_edit.html", 
        instrument=instrument, 
        instrument_types = instrument_types, 
        instrument_conditions=instrument_conditions,
        instrument_sizes = instrument_sizes,
        instrument_statuses = instrument_statuses,
        user=current_user) 


# Instrument View
@views.route('/instrument/view/<int:id>', methods=['GET','POST'])
@login_required
def instrument_view(id):
    instrument = Instrument.query.get_or_404(id)
    return render_template("instrument_edit.html", instrument=instrument, user=current_user)



###### Checkout ##########

def checkout_from_request(checkout,request):
    try:
        checkout.checkout_date = datetime.strptime(request.form['checkout_date'],'%Y-%m-%d')
    except: pass
    try:
        checkout.due_date = datetime.strptime(request.form['due_date'],'%Y-%m-%d')
    except: pass
    try:
        checkout.return_date = datetime.strptime(request.form['return_date'],'%Y-%m-%d')
    except: pass
    if(request.form.get('student_id') is not None):
        checkout.student_id = request.form.get('student_id')
    checkout.instrument_id = request.form.get('instrument_id')
    checkout.checkout_condition_id = request.form.get('checkout_condition')
    checkout.return_condition_id = request.form.get('return_condition')
    checkout.return_location = request.form.get('return_location')
    checkout.notes = request.form.get('notes')
    return checkout


def checkout_save(checkout,request):
    old_checkout_date = checkout.checkout_date
    old_return_date = checkout.return_date
    checkout_date = None
    due_date = None
    return_date = None
    try:
        checkout_date = datetime.strptime(request.form['checkout_date'],'%Y-%m-%d')
    except: pass
    try:
        due_date = datetime.strptime(request.form['due_date'],'%Y-%m-%d')
    except: pass
    try:
        return_date = datetime.strptime(request.form['return_date'],'%Y-%m-%d')
    except: pass

    checkout.student_id = request.form.get('student_id')
    checkout.instrument_id = request.form.get('instrument_id')
    checkout.checkout_date = checkout_date
    checkout.due_date = due_date
    checkout.return_date = return_date
    checkout.checkout_condition_id = request.form.get('checkout_condition')
    checkout.return_condition_id = request.form.get('return_condition')
    checkout.return_location = request.form.get('return_location')
    checkout.notes = request.form.get('notes')
    db.session.commit()
    if old_checkout_date is None and checkout_date is not None:
        flash(f'{checkout.student.first_name} {checkout.student.last_name} checked out {checkout.instrument.tag}:{checkout.instrument.type.name}', category='success')
    elif old_return_date is None and return_date is not None:
        flash(f'{checkout.student.first_name} {checkout.student.last_name} returned {checkout.instrument.tag}:{checkout.instrument.type.name}', category='success')
    else:
        flash(f'Instrument checkout updated: {old_return_date},{return_date}', category='success')
    return checkout

# Checkouts
@views.route('/checkouts', methods=['GET','POST'])
@login_required
def checkout_list():
    students = Student.query.all()
    return render_template("checkout_list.html",students=students, user=current_user)    

# Checkout Edit
@views.route('/checkout/edit/<int:id>', methods=['GET','POST'])
@login_required
def checkout_edit(id):
    checkout = StudentInstrument.query.get_or_404(id)
    available_instruments = Instrument.query.filter(or_(Instrument.status_id == 1, Instrument.id == checkout.instrument_id))
    semester = Semester.query.filter(
        datetime.now() >= Semester.earliest_checkout_date,
        datetime.now() <= Semester.latest_due_date 
        ).first()

    if request.method == 'GET':
        return render_template(
            "checkout_edit.html", 
            checkout = checkout, 
            semester = semester,
            instruments = available_instruments,
            students = Student.query.all(),
            instrument_conditions = InstrumentCondition.query.all(),
            user = current_user)

    if request.method == 'POST':
        old_checkout_date = checkout.checkout_date
        old_return_date = checkout.return_date
        checkout = checkout_from_request(checkout, request)
        db.session.add(checkout)

        # Update the instrument record to reflect the checkout status
        instrument = Instrument.query.get(checkout.instrument_id)
        if checkout.checkout_date is not None and checkout.return_date is None:
            instrument.status_id = 2
        elif checkout.return_date is not None:
            instrument.status_id = 1
        db.session.add(instrument)
        db.session.commit()        

        if old_checkout_date is None and checkout.checkout_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} checked out {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        elif old_return_date is None and checkout.return_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} returned {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        else:
            flash('Instrument checkout record updated.', category='success')

        return redirect(url_for('views.checkout_list'))


# Checkout New
@views.route('/checkout/new', methods=['GET','POST'])
@login_required
def checkout_new():
    available_instruments = Instrument.query.filter_by(status_id = 1)
    semester = Semester.query.filter(
        datetime.now() >= Semester.earliest_checkout_date,
        datetime.now() <= Semester.latest_due_date 
        ).first()
    checkout = StudentInstrument(
        checkout_date = datetime.strftime(datetime.now(),'%Y-%d-%m'),
        due_date = datetime.strftime(semester.latest_due_date,'%Y-%d-%m')
    )

    if request.method == 'GET':
        return render_template(
            "checkout_edit.html", 
            checkout = checkout, 
            semester = semester,
            instruments = available_instruments,
            students = Student.query.all(),
            instrument_conditions = InstrumentCondition.query.all(),
            user = current_user)

    if request.method == 'POST':
        checkout = checkout_from_request(checkout, request)
        db.session.add(checkout)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash(f' {checkout.instrument.type.name} {checkout.instrument.tag} is already checked out to {checkout.student.first_name} {checkout.student.last_name}', category='danger')
            return redirect(url_for('views.checkout_edit'))

        # Update the instrument record to reflect the checkout status
        instrument = Instrument.query.get(checkout.instrument_id)
        if checkout.checkout_date is not None and checkout.return_date is None:
            instrument.status_id = 2
        elif checkout.return_date is not None:
            instrument.status_id = 1
        db.session.add(instrument)
        db.session.commit()

        if checkout.checkout_date is not None and checkout.return_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} returned {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        elif checkout.checkout_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} checked out {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        else:
            flash('Instrument checkout record updated.', category='success')

        return redirect(url_for('views.checkout_list'))
