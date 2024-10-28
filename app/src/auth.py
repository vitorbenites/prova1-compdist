# src/auth.py
from werkzeug.security import check_password_hash, generate_password_hash
from flask_httpauth import HTTPBasicAuth
from src.models.profile import Profile

auth = HTTPBasicAuth()


# Authentication control
@auth.verify_password
def verify_password(username, password):
    user = Profile.query.filter(Profile.username == username).first()
    if user and check_password_hash(generate_password_hash(user.password), password):
        return username
    return None


# Protect the Flask-Admin using username/password strings and SQLAlchemy
def validate_authentication(username, password):
    user = Profile.query.filter(Profile.username == username).first()
    if user and check_password_hash(generate_password_hash(user.password), password):
        return True
    return False
