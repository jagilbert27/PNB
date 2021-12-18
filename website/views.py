import enum
import sys
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import pandas
from sqlalchemy.sql.expression import null
from .models import Note, Student
from . import db
import json
from datetime import date, datetime
from .models import User, Note, \
    Student, Instrument, StudentInstrument, InstrumentType, InstrumentSize, InstrumentCondition, InstrumentStatus, \
    Semester, StudentSemester, Campus, GuardianType, StudentGuardian, Person, PersonRole, PersonsRoles

views = Blueprint('views', __name__)

truthy = ['agree','yes','true','1']
falsey = ['disagree','no','false','0']


class InstrumentConditions(enum.Enum):
    New=5
    Good=4
    Fair=3
    Poor=2
    Broken=1
    Unknown=0

class InstrumentStatuses(enum.Enum):
    Available=1
    CheckedOut=2
    NeedsRepair=3
    BeingRepaired=4
    Decommisioned=5

class InstrumentTypes(enum.Enum):
    Fiddle=1
    Guitar=2
    Mandolin=3
    Banjo=4
    Bass=5
    Ukulele=6

class InstrumentSizes(enum.Enum):
    _14  = 1
    _12  = 2
    _34  = 3
    Full = 4

@views.route('/Fill', methods=['GET', 'POST'])
def fill():
    StudentInstrument.query.delete()
    Instrument.query.delete()
    Student.query.delete()
    InstrumentCondition.query.delete()
    InstrumentSize.query.delete()
    InstrumentType.query.delete()
    InstrumentStatus.query.delete()
    Semester.query.delete()
    StudentSemester.query.delete()
    Campus.query.delete()
    GuardianType.query.delete()
    StudentGuardian.query.delete()
    Person.query.delete()
    PersonRole.query.delete()
    PersonsRoles.query.delete()
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
    
    db.session.add(InstrumentCondition(id=InstrumentConditions.New.value, name='New'))
    db.session.add(InstrumentCondition(id=InstrumentConditions.Good.value, name='Good'))
    db.session.add(InstrumentCondition(id=InstrumentConditions.Fair.value, name='Fair'))
    db.session.add(InstrumentCondition(id=InstrumentConditions.Poor.value, name='Poor'))
    db.session.add(InstrumentCondition(id=InstrumentConditions.Broken.value, name='Broken'))

    db.session.add(InstrumentStatus(id=InstrumentStatuses.Available.value, name='Available for checkout'))
    db.session.add(InstrumentStatus(id=InstrumentStatuses.CheckedOut.value, name='Checked out to Student'))
    db.session.add(InstrumentStatus(id=InstrumentStatuses.NeedsRepair.value, name='Needs Repair'))
    db.session.add(InstrumentStatus(id=InstrumentStatuses.BeingRepaired.value, name='Out for Repair'))
    db.session.add(InstrumentStatus(id=InstrumentStatuses.Decommisioned.value, name='Decommissioned'))

    db.session.add(Instrument(type_id=InstrumentTypes.Fiddle.value, tag='F1', condition_id=InstrumentConditions.New.value, status_id=InstrumentStatuses.Available.value ))
    db.session.add(Instrument(type_id=InstrumentTypes.Guitar.value, tag='G1', condition_id=InstrumentConditions.New.value, status_id=InstrumentStatuses.Available.value  ))

    db.session.add(Student(external_id=-1, email='a@a.com',first_name='Alpha',last_name='A'))
    db.session.add(Student(external_id=-2, email='b@b.com',first_name='Bravo',last_name='B'))
    db.session.add(Student(external_id=-3, email='c@c.com',first_name='Charlie',last_name='C'))

    db.session.add(StudentInstrument(student_id=1, instrument_id=1, checkout_date=datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=1, instrument_id=2, checkout_date=datetime(2021,11,1)))
    db.session.add(StudentInstrument(student_id=2, instrument_id=1, checkout_date=datetime(2021,11,1)))

    db.session.add(Semester(id=1, name='Winter 2021', first_checkout_date = datetime(2021,10,1), last_due_date = datetime(2022, 2,1)))
    db.session.add(Semester(id=2, name='Spring 2022', first_checkout_date = datetime(2022, 2,2), last_due_date = datetime(2022, 6,1)))
    db.session.add(Semester(id=3, name='Summer 2022', first_checkout_date = datetime(2022, 6,2), last_due_date = datetime(2022,10,2)))

    # Campus
    db.session.add(Campus(id=1, name='LCMS'))
    db.session.add(Campus(id=2, name='Blackburn'))
    db.session.add(Campus(id=3, name='Long Branch'))

    # Student Semesters
    db.session.add(StudentSemester(id=1, student_id=1, semester_id=1, grade=6, campus_id=1 ))
    db.session.add(StudentSemester(id=2, student_id=1, semester_id=3, grade=7, campus_id=2 ))

    # Guadian Types
    db.session.add(GuardianType(id=1, dependent_name='child', guardian_name='parent'))
    db.session.add(GuardianType(id=2, dependent_name='grandchild', guardian_name='grandparent'))
    db.session.add(GuardianType(id=3, dependent_name='relative', guardian_name='relative'))

    # Guardians (persons)
    db.session.add(Person(id=1,name='Grandpa Adams'))
    db.session.add(Person(id=2,name='Grandma Adams'))

    # Person Roles
    db.session.add(PersonRole(id=1,name='Guardian'))
    db.session.add(PersonRole(id=2,name='Teacher'))
    db.session.add(PersonRole(id=3,name='Staff'))

    # Grandpa Adams is a guardian
    db.session.add(PersonsRoles(id=1,person_id=1,role_id=1))


    # Student Guardians
    db.session.add(StudentGuardian(id=1,student_id=1,guardian_id=1,guardian_type_id=2))
    db.session.add(StudentGuardian(id=2,student_id=1,guardian_id=2,guardian_type_id=2))
 
    # Person Roles

    db.session.commit()

    flash('DB initialized with test data')

    # Tests

    # Student
    student = Student.query.get(1)
    assert student.first_name == 'Alpha'

    # Semester
    semester = Semester.query.get(1)
    assert semester.name == 'Winter 2021'

    # Campus
    campus = Campus.query.get(3)
    assert campus.name == 'Long Branch'

    # StudentSemester:student
    assert student.semesters[0].semester.name == 'Winter 2021'
    assert semester.students[0].student.first_name == 'Alpha'

    # StudentSemester:Campus
    assert semester.students[0].campus_id == 1
    assert student.semesters[0].campus.name == 'LCMS'

    # Guardian Type
    guardian_type = GuardianType.query.get(2)
    assert guardian_type.dependent_name == 'grandchild'
    assert guardian_type.guardian_name == 'grandparent'

    # persons (Guardians)
    guardian = Person.query.get(1)
    guardian.name = 'Grandpa Adams'

    # StudentGuardian
    assert student.guardians[0].student_id == 1
    assert student.guardians[0].student.first_name == 'Alpha'
    assert student.guardians[0].guardian_id == 1
    assert student.guardians[0].guardian.name == 'Grandpa Adams'
    assert student.guardians[0].guardian_type_id == 2
    assert student.guardians[0].guardian_type.dependent_name == 'grandchild'
    assert student.guardians[0].guardian_type.guardian_name == 'grandparent'

    # Person Roles
    assert guardian.roles[0].role_id == 1
    assert guardian.roles[0].role.name == 'Guardian'

    #Role
    person_role = PersonRole.query.get(1)
    assert person_role.persons[0].id == 1
    assert person_role.persons[0].person.name == 'Grandpa Adams'

    # assert student.guardians[0].student.first_name == 'Alpha'

    flash('DB model tests pass')

    return redirect(url_for('views.home'))

# db.session.add(Role(id=1, name='dev'))
# db.session.add(UserRoles( user_id=1, role_id=1))


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
        students = Student.query.order_by(Student.external_id).all()
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
    db.session.commit()
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
    except: 
        checkout.checkout_date = None
    try:
        checkout.due_date = datetime.strptime(request.form['due_date'],'%Y-%m-%d')
    except:
        checkout.due_date = None
    try:
        checkout.return_date = datetime.strptime(request.form['return_date'],'%Y-%m-%d')
    except: 
        checkout.return_date = None
        
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
    if request.method == 'GET':
        students = Student.query.all()
        return render_template("checkout_list.html",students=students, today=date.today(), user=current_user)    

    checkout_id=request.form['id-to-delete']
    checkout = StudentInstrument.query.get(checkout_id)
    msg = f"Deleted {checkout.student.first_name}'s checkout of {checkout.instrument.type.name} {checkout.instrument.tag}"
    db.session.delete(checkout)
    db.session.commit()
    flash(msg, category='warning')
    return redirect(url_for('views.checkout_list'))


# Checkout Edit
@views.route('/checkout/edit/<int:id>', methods=['GET','POST'])
@login_required
def checkout_edit(id):
    checkout = StudentInstrument.query.get_or_404(id)
    available_instruments = Instrument.query.filter((Instrument.status_id == 1) | (Instrument.id == checkout.instrument_id))
    semester = Semester.query.filter(
        datetime.now() >= Semester.first_checkout_date,
        datetime.now() <= Semester.last_due_date 
        ).first()

    if request.method == 'GET':
        return render_template(
            "checkout_edit.html", 
            checkout = checkout, 
            semester = semester,
            instruments = available_instruments,
            students = Student.query.all(),
            instrument_conditions = InstrumentCondition.query.all(),
            readonly = False,
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
            if checkout.return_condition_id is not None:
                instrument.condition_id =  checkout.return_condition_id
            if checkout.return_location is not None:
                instrument.location = checkout.return_location
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
@views.route('/checkout/new/student/<int:student_id>', methods=['GET','POST'])
@views.route('/checkout/new/instrument/<int:instrument_id>', methods=['GET','POST'])
@views.route('/checkout/new/student/<int:student_id>/instrument/<int:instrument_id>', methods=['GET','POST'])
@login_required
def checkout_new(student_id=None,instrument_id=None):
    available_instruments = Instrument.query.filter_by(status_id = InstrumentStatuses.Available.value)
    semester = Semester.query.filter(
        datetime.now() >= Semester.first_checkout_date,
        datetime.now() <= Semester.last_due_date 
        ).first()
    checkout = StudentInstrument(
        student_id = student_id,
        instrument_id = instrument_id
    )
    if semester:
        checkout.checkout_date = datetime.strftime(datetime.now(),'%Y-%d-%m'),
        checkout.due_date = datetime.strftime(semester.last_due_date,'%Y-%d-%m'),

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
            instrument.status_id = InstrumentStatuses.CheckedOut.value
        elif checkout.return_date is not None:
            instrument.status_id = InstrumentStatuses.Available.value
        db.session.add(instrument)

        if checkout.checkout_date is not None and checkout.return_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} returned {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        elif checkout.checkout_date is not None:
            flash(f'{checkout.student.first_name} {checkout.student.last_name} checked out {checkout.instrument.type.name} {checkout.instrument.tag}', category='success')
        else:
            flash('Instrument checkout record updated.', category='success')

        db.session.commit()

        return redirect(url_for('views.checkout_list'))

# delete checkout
@views.route('/delete-checkout', methods=['POST'])
def checkout_delete():
    request_data = json.loads(request.data)
    checkout_id = request_data['checkout_id']
    checkout = StudentInstrument.query.get(checkout_id)
    msg = f'Checkout Deleted'
    if checkout:
        try:
            db.session.delete(checkout)
            db.session.commit()
            flash(msg, category='success')
        except BaseException as ex:
            db.session.rollback()
            flash(f'Delete Failed {type(ex)}', category='error')
    return jsonify({})


@views.route('/students/import', methods=['GET','POST'])
@login_required
def student_import():
    stats = {
        'students': {
            'total': 0,
            'added': 0,
            'updated': 0
        },
        'student_semesters': {
            'total': 0,
            'added': 0,
            'updated': 0
        },
        'checkouts': {
            'total': 0,
            'added': 0,
            'updated': 0
        },
    }

    # try:

    # import_table = pandas.read_csv('student_import.csv').transpose()
    parse_dates = ['Checkout Date', 'Due Date','Return Date']
    import_table = pandas.read_csv('student_import.csv',parse_dates=parse_dates).transpose()
    for _, imported in import_table.items():
        stats['students']['total'] += 1
        student=Student.query.filter(Student.external_id == imported['Record number']).first()
        if student:
            stats['students']['updated'] += 1
        else:
            stats['students']['added'] += 1
            student = Student()
            student.external_id = imported['Record number']

        # Student Data
        student.email = imported['Email']
        student.first_name = imported['First Name']
        student.last_name = imported['Last Name']
        student.address = imported['Address']
        student.phone = imported['Phone']
        db.session.add(student)

        # Hardcode the semester for now
        semester = Semester.query.filter(Semester.name == 'Winter 2021').first()

        # do we have that semester record for this student yet?
        stats['student_semesters']['total'] += 1
        student_semester = StudentSemester.query.filter(
            (StudentSemester.semester_id == semester.id) &            
            (StudentSemester.student_id == student.id)).first()
        if student_semester:
            stats['student_semesters']['updated'] += 1
        else:
            stats['student_semesters']['added'] += 1
            student_semester = StudentSemester()
            student_semester.external_id = imported['Record number']
            student_semester.student_id = student.id
            student_semester.semester_id = semester.id
        
        campus = Campus.query.filter(Campus.name == imported['Location']).first()
        if campus:
            student_semester.campus_id = campus.id
        student_semester.grade = imported['Grade']

        instrument_1 = InstrumentType.query.filter(InstrumentType.name == imported['Instrument']).first()
        if instrument_1:
            student_semester.first_choice_instrument_type_id = instrument_1.id
        instrument_2 = InstrumentType.query.filter(InstrumentType.name == imported['Second instrument']).first()
        if instrument_2:
            student_semester.second_choice_instrument_type_id = instrument_2.id
        
        student_semester.shirt_size = imported['Shirt Size']
        student_semester.behavior_agreement = imported['Behavior Agreement'].lower() in truthy
        student_semester.photo_permission = imported['Photo Permission'].lower() in truthy
        student_semester.hardship_requested = str(imported['Hardship request']).lower() in truthy
        student_semester.tuition_charged = imported['Tuition']
        db.session.add(student_semester)

        # if i have any checkout data
        if imported['Checkout Date']:
            instrument = Instrument.query.filter(Instrument.tag == imported['Instrument tag']).first()
            if instrument:
                checkout = StudentInstrument.query \
                    .order_by(StudentInstrument.checkout_date.desc()) \
                    .filter(
                        (StudentInstrument.student_id == student.id) &
                        (StudentInstrument.checkout_date) &
                        (not StudentInstrument.return_date)) \
                    .first()
                
                print(f'checkout: {checkout}', file=sys.stderr)

                if checkout:
                    stats['checkouts']['updated'] += 1
                else:
                    stats['checkouts']['added'] += 1
                    checkout = checkout = StudentInstrument()

                checkout.student_id = student.id
                checkout.external_id = imported['Record number']
                checkout.instrument_id = instrument.id

                if str(imported['Checkout Date']) != 'NaT':
                    checkout.checkout_date = imported['Checkout Date']

                if str(imported['Due Date']) != 'NaT':
                    checkout.due_date = imported['Due Date']

                if str(imported['Return Date']) != 'NaT':
                    checkout.return_date = imported['Return Date']

                db.session.add(checkout)

    db.session.commit()

    flash(f'Import Complete. '+
        f"Student Total: {stats['students']['total']}, Added: {stats['students']['added']}, Updated: {stats['students']['updated']}\n"+
        f"Semester Total: {stats['student_semesters']['total']}, Added: {stats['student_semesters']['added']}, Updated: {stats['student_semesters']['updated']}\n"+
        f"Checkouts Total: {stats['checkouts']['total']}, Added: {stats['checkouts']['added']}, Updated: {stats['checkouts']['updated']}\n", 
        category='success')

# except:
#     flash(f'Import Failed. '+
#         f'Student Total: {stats.students.total}, Added: {stats.students.added}, Updated: {stats.students.updated}<br/>'+
#         f'Semester Total: {stats.students.total}, Added: {stats.students.added}, Updated: {stats.students.updated}<br/>'+
#         f'Checkouts Total: {stats.students.total}, Added: {stats.students.added}, Updated: {stats.students.updated}<br/>', 
#         category='error')

    return redirect(url_for('views.student_list'))


@views.route('/instruments/import', methods=['GET','POST'])
@login_required
def instrument_import():
    num_updated = 0
    num_added = 0
    num_total = 0
    import_table = pandas.read_csv('instrument_import.csv').transpose()

    for _, imported in import_table.items():
        num_total += 1
        instrument=Instrument.query.filter(Student.external_id == imported['Record number']).first()
        if instrument:
            num_updated += 1
        else:
            num_added += 1
            instrument = Instrument()
            instrument.external_id = imported['Record number']

        instrument.tag = str(imported['Inventory number']).upper()
        
        if 'BS'  in instrument.tag: instrument.type_id = InstrumentTypes.Bass.value
        elif 'B' in instrument.tag: instrument.type_id = InstrumentTypes.Banjo.value
        elif 'F' in instrument.tag: instrument.type_id = InstrumentTypes.Fiddle.value
        elif 'G' in instrument.tag: instrument.type_id = InstrumentTypes.Guitar.value
        elif 'M' in instrument.tag: instrument.type_id = InstrumentTypes.Guitar.value
        elif 'U' in instrument.tag: instrument.type_id = InstrumentTypes.Ukulele.value

        size = str(imported['Size']).upper()
        if size == "":        instrument.size_id = InstrumentSizes.Full.value
        elif size == "FULL":  instrument.size_id = InstrumentSizes.Full.value
        elif "03/04" in size: instrument.size_id = InstrumentSizes._34.value
        elif "3/4" in size:   instrument.size_id = InstrumentSizes._34.value
        elif "3.4" in size:   instrument.size_id = InstrumentSizes._34.value
        elif ".75" in size:   instrument.size_id = InstrumentSizes._34.value
        elif "01/02" in size: instrument.size_id = InstrumentSizes._12.value
        elif "1/2" in size:   instrument.size_id = InstrumentSizes._12.value
        elif "1.2" in size:   instrument.size_id = InstrumentSizes._12.value
        elif ".5" in size:    instrument.size_id = InstrumentSizes._12.value
        elif "01/04" in size: instrument.size_id = InstrumentSizes._14.value
        elif "1/4" in size:   instrument.size_id = InstrumentSizes._14.value
        elif "1.4" in size:   instrument.size_id = InstrumentSizes._14.value
        elif ".25" in size:   instrument.size_id = InstrumentSizes._14.value

        instrument.status_id = InstrumentStatuses.Available.value
        instrument.condition_id = InstrumentConditions.Good.value
        instrument.notes = (str(imported['Condition']).replace('nan','') + ' ' + str(imported['History']).replace('nan','')).strip()
        instrument.serial = str(imported['Serial number']).replace('nan','')
        instrument.brand = str(imported['Kind']).replace('nan','')
        instrument.location = str(imported['Location']).replace('nan','')
        db.session.add(instrument)

    db.session.commit()

    flash(f'Instrument Import Complete. Total: {num_total}, Updated: {num_updated}, Added: {num_added}', category='success')
    return redirect(url_for('views.instrument_list'))
