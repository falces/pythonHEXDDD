from os import environ
from flask import Flask
from flask_migrate import Migrate
from Infrastructure.Persistence.database import db


def configureDatabase(app: Flask):
    """
    Configura la base de datos SQLAlchemy y las migraciones.
    
    Args:
        app: Instancia de Flask
        
    Returns:
        Instancia de SQLAlchemy
    """
    mysql_local = 'mysql+mysqlconnector://'
    mysql_local += environ.get('MYSQL_USER')
    mysql_local += ':' + environ.get('MYSQL_PASSWORD')
    mysql_local += '@' + environ.get('SERVICE_NAME') + '_db'
    mysql_local += ':' + environ.get('MYSQL_INTERNAL_PORT')
    mysql_local += '/' + environ.get('MYSQL_DATABASE')

    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la instancia global de db con la app
    db.init_app(app)
    app.config.db = db

    # Configurar migraciones
    Migrate(
        app,
        db,
        directory='Shared/Infrastructure/Migrations'
    )

    return db