from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

# User Model for Authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Patient Model for Dataset Integration
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Float, nullable=False)
    hypertension = db.Column(db.Integer, nullable=False)
    # ever_married = db.Column(db.String(10), nullable=False)
    # work_type = db.Column(db.String(50), nullable=False)
    # residence_type = db.Column(db.String(10), nullable=False)
    avg_glucose_level = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    # smoking_status = db.Column(db.String(50), nullable=True)
    # stroke = db.Column(db.Integer, nullable=False)
