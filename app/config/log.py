import logging
from flask import Flask, request

def configureLogs(app: Flask):
    logFormatter = logging.Formatter("%(asctime)s %(pathname)-60.60s %(funcName)-20.20s %(lineno)-4d [%(levelname)-1.5s]  %(message)s")
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
        if str(response.status_code).startswith('3') is False:
            app.logger.info("%s on [%s] %s", response.status_code, request.method, request.url)
        return response