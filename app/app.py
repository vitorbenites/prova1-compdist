import logging
from flask import Flask, Response, redirect, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

# Application log
logging.basicConfig(format='%(asctime)s - %(message)s',
                    filename="log/app.log", level=logging.INFO)
log = logging.getLogger()

# Web Application name
app = Flask("Comp Dist")
auth = HTTPBasicAuth()

# Configuration
app.config.from_pyfile('cfg/app.cfg', silent=True)
app.config['FLASK_SECRET'] = app.config.get('SECRET_KEY')
app.config['BASIC_AUTH_FORCE'] = True
app.secret_key = app.config.get('SECRET_KEY')

# Set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

# adding configuration for using a database
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,
                         nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=True)
    registered = db.Column(db.DateTime(timezone=True), default=db.func.now())

    # repr method represents how one object of this datatable will look like
    def __repr__(self):
        return f"{self.username}"


# Authentication control
@auth.verify_password
def verify_password(username, password):
    user = Profile.query.filter(Profile.username == username)

    if user.all():
        user_query = user.all()[0]
        if check_password_hash(generate_password_hash(user_query.password), password):
            return username


# Protect the Flask-Admin using username/password strings and SQLAlchemy
def validate_authentication(username, password):
    user = Profile.query.filter(Profile.username == username)

    if user.all():
        user_query = user.all()[0]
        if user_query.password == password:
            return True
        return False
    return False


# Add administrative views here
class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class MyModelView(ModelView):
    def is_accessible(self):
        if auth.get_auth():
            username = auth.get_auth()['username']
            password = auth.get_auth()['password']
        else:
            username = None
            password = None

        if username and password:
            if validate_authentication(username, password) and username in app.config.get('ADMINISTRATORS'):
                return True
            else:
                raise AuthException('Not authenticated.')
        else:
            raise AuthException('Not authenticated.')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(auth.login_required())


class ProfileView(MyModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', ]
    can_export = True
    can_view_details = True


# Admin Interface
admin = Admin(app, name='Super App', template_mode='bootstrap4')
admin.add_view(ProfileView(Profile, db.session))


# Routes
@app.route('/')
@auth.login_required
def index():
    user = auth.current_user()

    # Check if the user exist
    user_db = Profile.query.filter(Profile.username == user)

    # Avoid error while checking the users in database
    user_list = False
    try:
        user_list = user_db.all()[0]
    except IndexError:
        pass

    if user_list:
        message_info = f"Usuário {user}, acessou o index."

        response = {"success": message_info}
        log.info(message_info)

        return jsonify(response)


# Initialize the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True, port=8080)
