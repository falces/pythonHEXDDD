import logging
from flask import Flask, request

def configureLogs(app: Flask):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("{0}/{1}.log".format('./log', 'app'), encoding='locale')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Avoid APP logs
    logging.getLogger('werkzeug').disabled = True

    @app.after_request
    def after_request(response):
        app.logger.info("%s on [%s] %s", response.status_code, request.method, request.url)
        return response