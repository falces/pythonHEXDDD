from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def configureDatabase(app: Flask):
    mysql_local = 'mysql+mysqlconnector://' + environ.get('MYSQL_USER') + ':' + environ.get('MYSQL_PASSWORD') + '@pt_db:3306/pythontemplate'
    # mysql_local = 'mysql+mysqlconnector://thirdpl:thirdpl@localhost:13306/ThirdPL'

    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    app.config.db = db

    Migrate(
        app,
        app.config.db,
        directory='Shared/Infrastructure/Migrations'
    )

    return db