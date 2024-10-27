# src/views/index.py
from flask import Blueprint, jsonify
from src.models.profile import Profile
from src.auth import auth
from src.log import log

# Blueprint para rotas públicas e de usuário
index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
@auth.login_required
def index():
    user = auth.current_user()

    # Verifica se o usuário existe no banco de dados
    user_db = Profile.query.filter(Profile.username == user)

    user_list = False
    try:
        user_list = user_db.all()[0]
    except IndexError:
        pass

    if user_list:
        message_info = f"Usuário {user} acessou o index."
        response = {"success": message_info}
        log.info(message_info)
        return jsonify(response)
