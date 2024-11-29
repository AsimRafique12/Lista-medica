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

@main.route('/add_patient_submitted', methods=['POST'])
def add_patient_submitted():
    if request.method == 'POST':
        # Capture form data
        age = request.form.get('age')
        gender = request.form.get('gender')
        hypertension = request.form.get('hypertension')  # Ensure it is integer (0 or 1)
        avg_glucose_level = request.form.get('avg_glucose_level')  # Ensure float for proper calculation
        bmi = request.form.get('bmi')  # Ensure float for BMI

        # Validate form fields
        if not age or not gender or not hypertension or not avg_glucose_level or not bmi:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.goto_add_patient'))

        try:
            # Cast data to correct types
            age = int(age)
            hypertension = int(hypertension)  # Convert hypertension to integer (0 or 1)
            avg_glucose_level = float(avg_glucose_level)  # Convert to float for proper calculation
            bmi = float(bmi)

            # Create a new patient record
            new_patient = Patient(
                age=age,
                gender=gender,
                hypertension=hypertension,
                avg_glucose_level=avg_glucose_level,
                bmi=bmi
            )

            # Try adding to the database
            db.session.add(new_patient)
            db.session.commit()  # Commit changes to the database
            flash('Patient registered successfully!', 'success')
            return redirect(url_for('main.goto_add_patient'))  # Redirect after successful submission
        except ValueError:
            flash('Please enter valid numeric values for age, glucose level, and BMI.', 'danger')
            return redirect(url_for('main.goto_add_patient'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')  # Flash error message if something goes wrong
            db.session.rollback()  # Rollback in case of error to maintain database consistency
            return redirect(url_for('main.goto_add_patient'))  # Redirect back to form

    return render_template('register_patient.html')

@main.route('/gotopatients')
def gotopatients():
    records = Patient.query.all()  # Query all patient records from the database
    return render_template('view_records.html', records=records)

@main.route('/gotoeditpatients')
def gotoeditpatients():
    return render_template('edit_patient.html')

@main.route('/gotoregister')
def gotoregister():
    return render_template('register.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hash password before storing
        db.session.add(user)
        db.session.commit()  # Commit user to the database
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))  # Redirect to login page after successful registration
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Check if the password matches
            login_user(user)
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard after login
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    patients = Patient.query.all()  # Fetch all patient records
    return render_template('dashboard.html', patients=patients)

@main.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the current user
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))  # Redirect to login page after logging out

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
            db.session.commit()  # Commit the changes to the database
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('main.gotopatients'))  # Redirect after successful update
        except Exception as e:
            flash(f'Error updating patient: {e}', 'danger')  # Handle any errors
            db.session.rollback()  # Rollback if there is an error

    return render_template('edit_patient.html', patient=patient)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    # Fetch the patient record by ID
    patient = Patient.query.get_or_404(id)

    try:
        db.session.delete(patient)  # Delete the patient record
        db.session.commit()  # Commit the changes to the database
        flash('Patient deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting patient: {e}', 'danger')  # Handle any errors during deletion
        db.session.rollback()  # Rollback if there is an error

    return redirect(url_for('main.gotopatients'))  # Redirect to the list of patients after deletion
