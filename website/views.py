from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Student, Instrument, StudentInstrument, InstrumentType, InstrumentSize, InstrumentCondition, InstrumentStatus
from . import db
import json
import sqlalchemy
import datetime

views = Blueprint('views', __name__)

@views.route('/Fill', methods=['GET', 'POST'])
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

    db.session.commit()
    db.session.add(Instrument(type_id=1, tag='F1', condition_id=3, status_id=1 ))
    db.session.add(Instrument(type_id=2, tag='G1', condition_id=4 ))
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


# student   list
# student/edit/id  = edit
# student/view/id  = view
# student/new


# Student List
@views.route('/students', methods=['GET'])
@login_required
def student_list():
    students = Student.query.all()
    return render_template("student_list.html", students=students, user=current_user)

# Student New
@views.route('/student/new', methods=['GET','POST'])
@login_required
def student_new():
    if request.method == 'GET':
        return render_template("student_edit.html", student=Student(), user=current_user)

    if request.method == 'POST':
        try:
            student = Student(
                first_name = request.form.get('first_name'),
                last_name = request.form.get('last_name'),
                email = request.form.get('email'),
                )
            db.session.add(student)
            db.session.commit()
            flash(f'Added Student {student.first_name} {student.last_name}', category='success')
            return redirect(url_for('views.student_list'))
        except sqlalchemy.exc.IntegrityError as ex:
            db.session.rollback()
            flash(f'Save Failed {type(ex)}', category='error')

# Student Edit
@views.route('/student/edit/<int:id>', methods=['GET','POST'])
@login_required
def student_edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("student_edit.html", student=student, user=current_user)
    
    if request.method == 'POST':
        student.email = request.form.get('email')
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        db.session.commit()
        flash(f'Updated Student {student.first_name} {student.last_name}', category='success')
        return redirect(url_for('views.student_list'))

# Student New
@views.route('/student/view/<int:id>', methods=['GET'])
@login_required
def student_view(id):
    student = Student.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("student_view.html", student=student, user=current_user)

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


# Checkouts
@views.route('/checkouts', methods=['GET','POST'])
@login_required
def checkout_list():
    students = Student.query.all()

    # msg = "Student structure:<br/><br/>"
    # for student in students:
    #     msg += f'Student.first_name: {student.first_name} <br/>'
    #     for checkout in student.checkouts:
    #         msg += f'    Checkout Date {checkout.checkout_date.strftime("%m/%d/%Y")} <br/>'
    #         msg += f'        Type: {checkout.instrument.type} <br/><br/>'
    # return msg

    return render_template("checkout_list.html",students=students, user=current_user)    


# Checkout Edit
@views.route('/checkout/edit/<int:id>', methods=['GET','POST'])
@login_required
def checkout_edit(id):
    checkout = StudentInstrument.query.get_or_404(id)
    instruments = Instrument.query.all()
    students = Student.query.all()
    instrument_conditions = InstrumentCondition.query.all()

    if request.method == 'GET':
        return render_template(
            "checkout_edit.html", 
            checkout=checkout, 
            instruments = instruments,
            students = students,
            instrument_conditions = instrument_conditions,
            user=current_user)
    
    # if request.method == 'POST':
    #     student.email = request.form.get('email')
    #     student.first_name = request.form.get('first_name')
    #     student.last_name = request.form.get('last_name')
    #     db.session.commit()
    #     flash('Student Updated!', category='success')
    #     return redirect(url_for('views.checkout_list'))