# src/__init__.py
import os
from flask import Flask
from flask_migrate import Migrate
from src.database import db
from src.views import admin_blueprint, index_blueprint
from src.models.profile import Profile
from src.views.admin import admin

# Instância da aplicação Flask
app = Flask("Comp Dist")

# Configuração do Flask
app.config['FLASK_SECRET'] = os.getenv('SECRET_KEY')
app.secret_key = os.getenv('SECRET_KEY')
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'
app.config['BASIC_AUTH_FORCE'] = True

# Construção da URI do banco de dados
db_type = os.getenv('DATABASE_TYPE', 'sqlite').lower()
db_name = os.getenv('DATABASE_NAME', 'usersdb')

# Alternar entre bancos de dados
if db_type == 'mysql':
    user = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASSWORD')
    port = os.getenv('MYSQL_PORT', 3306)
    host = os.getenv('MYSQL_HOST', 'localhost')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{
        user}:{password}@{host}:{port}/{db_name}'
elif db_type == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.sqlite3'

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)

# Migrations
migrate = Migrate(app, db)

# Registro dos blueprints
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(index_blueprint, url_prefix='/')
admin.init_app(app)

# Inicialização do banco de dados
with app.app_context():
    db.create_all()

    # Verifica se a tabela `profiles` já possui registros
    if Profile.query.count() == 0:
        # Obtém as credenciais do administrador do arquivo de configuração
        admin_username = os.getenv('ADMIN_USER')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if admin_username and admin_password:
            existing_admin = Profile.query.filter_by(
                username=admin_username).first()

            if not existing_admin:
                admin_user = Profile(
                    username=admin_username, password=admin_password)
                db.session.add(admin_user)
                db.session.commit()
                print(f"Usuário administrador '{
                      admin_username}' criado com sucesso.")
            else:
                print("O usuário administrador já existe.")
