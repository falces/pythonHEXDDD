from flask import Flask
from werkzeug.exceptions import HTTPException
import traceback

def exceptionHandler(app: Flask):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, (HTTPException)):
            exceptionCode = e.code
        else:
            exceptionCode = 500
        exceptionMessage = str(e)
        response = {
                    "error": exceptionMessage,
                    "code": exceptionCode,
                    "traceback": traceback.format_exc()
                }
        app.logger.error(exceptionMessage)
        return response, exceptionCode