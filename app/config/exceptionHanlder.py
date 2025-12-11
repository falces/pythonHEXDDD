from flask import Flask
import traceback
from os import environ


def exceptionHandler(app: Flask):
    @app.errorhandler(Exception)
    def handle_exception(e):  
        exceptionCode = 500
        if hasattr(e, 'code') and isinstance(e.code, int) and 100 <= e.code < 600:
            exceptionCode = e.code
        
        exceptionMessage = str(e)
        
        response = {
                "error": exceptionMessage,
                "code": exceptionCode,
            }
        
        if environ.get('ENVIRONMENT') == 'dev':
            response["traceback"] = traceback.format_exc()
        
        app.logger.error(exceptionMessage)
        return response, exceptionCode
