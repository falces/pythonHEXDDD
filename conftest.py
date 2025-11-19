"""
Configuración de pytest y fixtures globales.
Este archivo es ejecutado automáticamente por pytest antes de correr los tests.
"""

import sys
import os
from pathlib import Path

import pytest
from flask import Flask
from dotenv import load_dotenv

# Cargar variables de entorno para tests
env_test_path = Path(__file__).parent / ".env.test"
if env_test_path.exists():
    load_dotenv(env_test_path)
else:
    # Valores por defecto si no existe .env.test
    os.environ.setdefault('MYSQL_HOST', 'localhost')
    os.environ.setdefault('MYSQL_PORT', '3306')
    os.environ.setdefault('MYSQL_INTERNAL_PORT', '3306')
    os.environ.setdefault('MYSQL_DATABASE', 'test_db')
    os.environ.setdefault('MYSQL_USER', 'test_user')
    os.environ.setdefault('MYSQL_PASSWORD', 'test_password')
    os.environ.setdefault('SERVICE_NAME', 'test_service')
    os.environ.setdefault('STREAM_AVAILABILITY_HOST', 'https://api.test.com')
    os.environ.setdefault('STREAM_AVAILABILITY_KEY', 'test_key')

# Agregar el directorio app al path
app_path = Path(__file__).parent / "app"
sys.path.insert(0, str(app_path))


@pytest.fixture(scope='session')
def app():
    """
    Fixture que crea una instancia de Flask para testing.
    Scope 'session' significa que se crea una vez para toda la sesión de tests.
    """
    from app import app as flask_app

    # Configuración específica para tests
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Base de datos en memoria
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
    })

    yield flask_app


@pytest.fixture(scope='function')
def client(app):
    """
    Fixture que proporciona un cliente de test para hacer requests HTTP.
    Scope 'function' significa que se crea uno nuevo para cada test.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def app_context(app):
    """
    Fixture que proporciona el contexto de la aplicación Flask.
    Necesario para acceder a current_app, db.session, etc.
    """
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db_session(app_context):
    """
    Fixture que proporciona una sesión de base de datos limpia para cada test.
    Hace rollback automático después de cada test.
    """
    from Infrastructure.Persistence.database import db

    # Crear todas las tablas
    db.create_all()

    yield db.session

    # Limpiar después del test
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio para tests unitarios.
    Permite acceso a métodos adicionales como find_by_id para backward compatibility.
    """
    from unittest.mock import Mock

    # Creamos mock sin spec estricto para permitir find_by_id
    mock_repo = Mock()
    mock_repo.save = Mock()
    mock_repo.delete = Mock()
    mock_repo.find_by_id = Mock()

    return mock_repo


@pytest.fixture(scope='function')
def mock_event_dispatcher():
    """
    Fixture que proporciona un mock del event dispatcher.
    """
    from unittest.mock import Mock
    from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher

    return Mock(spec=EventDispatcher)


@pytest.fixture(scope='function')
def sample_greeting_text():
    """
    Fixture que proporciona texto de ejemplo para greetings.
    """
    return "Hello World"


@pytest.fixture(scope='function')
def sample_hello_world():
    """
    Fixture que proporciona una entidad HelloWorld de ejemplo.
    """
    from Domain.HelloWorld.HelloWorld import HelloWorld
    from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject

    greeting = GreetingValueObject.create("Test Greeting")
    hello_world = HelloWorld.create(greeting=greeting)
    hello_world._id = 1

    return hello_world
