from cryptography.fernet import Fernet
import re

SECRET_KEY = Fernet.generate_key()
fernet = Fernet(SECRET_KEY)

def encrypt_data(data):
    return {key: fernet.encrypt(value.encode()).decode() for key, value in data.items()}

def validate_input(data):
    # Example: validate email
    return re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email'))
