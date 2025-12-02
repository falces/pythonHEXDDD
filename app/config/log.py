import logging
from flask import Flask, request

# Logger global que se puede importar sin importaciones circulares
logger = logging.getLogger(__name__)


def configureLogs(app: Flask):
    """
    Configura el sistema de logs de la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    logFormatter = logging.Formatter("%(asctime)s %(pathname)-60.60s %(funcName)-20.20s %(lineno)-4d [%(levelname)-1.5s]  %(message)s")
    rootLogger = logging.getLogger()
    
    # Configurar nivel de log
    rootLogger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("{0}/{1}.log".format('./log', 'app'), encoding='locale')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Avoid APP logs
    logging.getLogger('werkzeug').disabled = True
    logging.getLogger("mysql.connector").setLevel(logging.WARNING)

    @app.after_request
    def after_request(response):
        if str(response.status_code).startswith('3') is False:
            app.logger.info("%s on [%s] %s", response.status_code, request.method, request.url)
        return response