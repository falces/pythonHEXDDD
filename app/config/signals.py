from flask import Flask
from flask.signals import Namespace

def configureSignals(app: Flask):
    namespace = Namespace()

    return {
        "new_hello_world": namespace.signal("new_hello_world"),
    }