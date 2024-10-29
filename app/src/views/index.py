# src/views/index.py
from flask import Blueprint, jsonify
from src.models.profile import Profile
from src.auth import auth
from src.logger import log

# Blueprint para rotas públicas e de usuário
index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
@auth.login_required
def index():
    # Obtém o nome do usuário atual
    user = auth.current_user()

    if user is None:
        return jsonify({"error": "User not authenticated"}), 401

    # Verifica se o usuário existe no banco de dados
    user_db = Profile.query.filter_by(username=user).first()

    if user_db:
        message_info = f"Usuario {user} acessou o index."
        response = {"success": message_info}
        log.info(message_info)
        return jsonify(response)
    else:
        return jsonify({"error": "User not found in database"}), 404
