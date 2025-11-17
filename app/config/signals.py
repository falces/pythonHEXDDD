from flask import Flask
from flask.signals import Namespace

# Instancia global de signals
# Se inicializa en configureSignals() y se puede importar sin ciclos
namespace = Namespace()
signals = {
    "new_hello_world": namespace.signal("new_hello_world"),
}


def configureSignals(app: Flask):
    """
    Configura las señales de la aplicación.
    Ahora solo retorna la referencia global para mantener compatibilidad.
    
    Args:
        app: Instancia de Flask
        
    Returns:
        dict: Diccionario de señales configuradas
    """
    return signals