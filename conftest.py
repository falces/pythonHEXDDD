"""
Configuración de pytest y fixtures globales.
Este archivo es ejecutado automáticamente por pytest antes de correr los tests.
"""

import sys
import os
from pathlib import Path

import pytest
from flask import Flask

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
    """
    from unittest.mock import Mock
    from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
    
    return Mock(spec=HelloWorldRepositoryInterface)


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
    from Domain.HelloWorld.ValueObjects.Greeting import Greeting
    
    greeting = Greeting.create("Test Greeting")
    hello_world = HelloWorld.create(greeting=greeting)
    hello_world._id = 1
    
    return hello_world
