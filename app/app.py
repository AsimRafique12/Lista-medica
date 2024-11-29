from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Set secret key for flash messages and sessions
app.config['SECRET_KEY'] = 'your_secret_key'

# Set up your database URI (using SQLite here, you can change to PostgreSQL, MySQL, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database in the current directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define a simple model (User table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Route for testing the database
@app.route('/')
def index():
    users = User.query.all()  # Query all users
    return f"Users: {users}"  # Display all users in the database

if __name__ == '__main__':
    app.run(debug=True)
