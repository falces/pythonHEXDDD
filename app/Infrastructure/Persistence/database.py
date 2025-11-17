"""
Módulo central para la instancia de SQLAlchemy.
Este módulo evita importaciones circulares al proporcionar
una referencia central a la base de datos.
"""

from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
# Se inicializa en app.py con db.init_app(app)
db = SQLAlchemy()
