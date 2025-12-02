from os import environ
from flask import Flask
from flask_migrate import Migrate
from Shared.Infrastructure.Persistence.database import db


def configureDatabase(app: Flask):
    """
    Configura la base de datos SQLAlchemy y las migraciones.

    Args:
        app: Instancia de Flask

    Returns:
        Instancia de SQLAlchemy
    """
    # Usar SQLALCHEMY_DATABASE_URI si está definida (para tests)
    # De lo contrario, construir la cadena de conexión MySQL
    database_uri = environ.get('SQLALCHEMY_DATABASE_URI')

    if not database_uri:
        mysql_local = 'mysql+mysqlconnector://'
        mysql_local += environ.get('MYSQL_USER')
        mysql_local += ':' + environ.get('MYSQL_PASSWORD')
        mysql_local += '@' + environ.get('SERVICE_NAME') + '_db'
        mysql_local += ':' + environ.get('MYSQL_INTERNAL_PORT')
        mysql_local += '/' + environ.get('MYSQL_DATABASE')
        database_uri = mysql_local

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
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
