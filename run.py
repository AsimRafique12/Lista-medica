from app import create_app, db
from app.models import User, Patient

app = create_app()

with app.app_context():
    db.create_all()  # Ensure database tables are created

if __name__ == "__main__":
    app.run(debug=True, port=5001)
