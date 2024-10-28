# src/views/admin.py
import os
from flask import Blueprint, redirect, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException
from src.models.profile import Profile
from src.auth import auth, validate_authentication
from src.database import db

# Blueprint para rotas de administração
admin_blueprint = Blueprint('admin_routes', __name__)


# Classe para personalizar a exibição de modelos no painel Admin
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
            if validate_authentication(username, password) and username == os.getenv('ADMIN_USER'):
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


# Configuração do Flask-Admin
admin = Admin(name='Super App', template_mode='bootstrap4')
admin.add_view(ProfileView(Profile, db.session))
