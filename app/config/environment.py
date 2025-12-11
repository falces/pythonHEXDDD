from os import environ
from flask import Flask

def configureEnvironment(app: Flask):
    app.config.update(
        STREAM_AVAILABILITY_HOST = environ.get('STREAM_AVAILABILITY_HOST'),
        STREAM_AVAILABILITY_KEY = environ.get('STREAM_AVAILABILITY_KEY'),
        ENVIRONMENT = environ.get('ENVIRONMENT'),
    )