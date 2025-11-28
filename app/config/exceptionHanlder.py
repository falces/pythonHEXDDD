from flask import Flask
import traceback


def exceptionHandler(app: Flask):
    @app.errorhandler(Exception)
    def handle_exception(e):
        exceptionCode = e.code if hasattr(e, 'code') else 500
        exceptionMessage = str(e)
        response = {
            "error": exceptionMessage,
            "code": exceptionCode,
            "traceback": traceback.format_exc()
        }
        app.logger.error(exceptionMessage)
        return response, exceptionCode
