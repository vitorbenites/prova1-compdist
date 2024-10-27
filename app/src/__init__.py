# src/__init__.py
from flask import Flask
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from src.database import db
from src.views import admin_blueprint, index_blueprint
from src.models.profile import Profile
from src.views.admin import admin

# Instâncias do Flask, banco de dados e autenticação
app = Flask("Comp Dist")

# Configuração
app.config.from_pyfile('cfg/app.cfg', silent=True)
app.config['FLASK_SECRET'] = app.config.get('SECRET_KEY')
app.config['BASIC_AUTH_FORCE'] = True
app.secret_key = app.config.get('SECRET_KEY')
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)
# Migrate
migrate = Migrate(app, db)

# Registro dos blueprints
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(index_blueprint)
admin.init_app(app)

# Inicialização do banco de dados
with app.app_context():
    # Tenta criar o banco de dados
    try:
        db.create_all()
        print("Banco de dados criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")

    # Verifica se a tabela `profiles` já possui registros
    if Profile.query.count() == 0:
        # Obtém as credenciais do administrador do arquivo de configuração
        admin_username = app.config.get('ADMIN_USERNAME')
        admin_password = app.config.get('ADMIN_PASSWORD')

        if admin_username and admin_password:
            # Verifica se o usuário admin já está registrado
            existing_admin = Profile.query.filter_by(
                username=admin_username).first()

            if not existing_admin:
                # Cria o hash da senha do administrador e adiciona o usuário ao banco
                # hashed_password = generate_password_hash(admin_password)
                admin_user = Profile(
                    username=admin_username, password=admin_password)
                db.session.add(admin_user)
                db.session.commit()
                print(f"Usuário administrador '{
                      admin_username}' criado com sucesso.")
            else:
                print("O usuário administrador já existe.")
