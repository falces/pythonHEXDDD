from os import environ
from flask import Flask

def configureEnvironment(app: Flask):
    app.config.update(
        STREAM_AVAILABILITY_HOST = environ.get('STREAM_AVAILABILITY_HOST'),
        STREAM_AVAILABILITY_KEY = environ.get('STREAM_AVAILABILITY_KEY'),
        RABBITMQ_USER = environ.get('RABBITMQ_USER'),
        RABBITMQ_PASS = environ.get('RABBITMQ_PASS'),
        RABBITMQ_HOST = environ.get('RABBITMQ_HOST'),
        RABBITMQ_PORT = environ.get('RABBITMQ_PORT'),
        RABBITMQ_VHOST = environ.get('RABBITMQ_VHOST'),
    )