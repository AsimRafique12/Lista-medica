from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Patient
from app.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/goto_add_patient')
def goto_add_patient():
    return render_template('register_patient.html')

@main.route('/add_patient_submitted', methods = { 'POST' })
def add_patient_submitted():
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        hypertension = int(request.form.get('hypertension'))
        avg_glucose_level = float(request.form.get('avg_glucose_level'))
        bmi = float(request.form.get('bmi'))

        # Create a new patient record
        new_patient = Patient(
            age=age,
            gender=gender,
            hypertension=hypertension,
            avg_glucose_level=avg_glucose_level,
            bmi=bmi
        )

        # Add to the database
        try:
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient registered successfully!', 'success')
            return redirect(url_for('main.goto_add_patient'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            db.session.rollback()
            return redirect(url_for('main.goto_add_patient'))

    return render_template('register_patient.html')


@main.route('/gotopatients')
def gotopatients():
    records = Patient.query.all()
    return render_template('view_records.html', records = records)

@main.route('/gotoeditpatients')
def gotoeditpatients():
    return render_template('edit_patient.html')

@main.route('/gotoregister')
def gotoregister():
    return render_template('register.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful. Please log in.', 'success')
    return redirect(url_for('main.login'))
    # return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/')
@login_required
def dashboard():
    patients = Patient.query.all()  # Fetch all patient records
    return render_template('dashboard.html', patients=patients)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    # Fetch the patient record by ID
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        # Update patient information from form data
        patient.age = request.form.get('age')
        patient.gender = request.form.get('gender')
        patient.hypertension = int(request.form.get('hypertension'))
        patient.avg_glucose_level = float(request.form.get('avg_glucose_level'))
        patient.bmi = float(request.form.get('bmi'))

        try:
            db.session.commit()
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('main.view_records'))
        except Exception as e:
            flash(f'Error updating patient: {e}', 'danger')
            db.session.rollback()

    return render_template('edit_patient.html', patient=patient)
