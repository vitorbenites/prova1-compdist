# src/__init__.py
from flask import Flask
from flask_migrate import Migrate
from src.database import db
from src.views import admin_blueprint, index_blueprint

# Instâncias do Flask, banco de dados e autenticação
app = Flask("Comp Dist")
migrate = Migrate(app, db)

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

# Registro dos blueprints
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(index_blueprint)

# Inicialização do banco de dados
with app.app_context():
    db.create_all()
