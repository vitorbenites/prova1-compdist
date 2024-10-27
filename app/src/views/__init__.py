# app/views/__init__.py
from src.views.admin import admin_blueprint
from src.views.index import index_blueprint

# Aqui é onde registramos os blueprints no app principal.
__all__ = ['admin_blueprint', 'index_blueprint']
