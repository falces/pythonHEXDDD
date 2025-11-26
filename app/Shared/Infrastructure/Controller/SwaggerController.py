"""
Controlador para servir la documentación Swagger UI.
"""

from flask import Blueprint, send_from_directory, make_response
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Blueprint para servir archivos estáticos de OpenAPI
swagger_static = Blueprint('swagger_static', __name__)

# Configuración de Swagger UI
SWAGGER_URL = '/api/docs'  # URL donde estará disponible Swagger UI
API_URL = '/api/docs/openapi.yaml'  # URL del archivo OpenAPI spec

# Blueprint de Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PythonHEXDDD API",
        'layout': 'BaseLayout',
        'deepLinking': True,
        'displayRequestDuration': True,
        'docExpansion': 'list',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
        'syntaxHighlight.theme': 'monokai'
    }
)


@swagger_static.route('/api/docs/openapi.yaml')
def serve_openapi_spec():
    """
    Sirve el archivo de especificación OpenAPI.
    """
    # SwaggerController.py está en: app/Shared/Infrastructure/Controller/
    # APIDocs está en: app/APIDocs/
    current_dir = os.path.dirname(__file__)
    # Subir 3 niveles: Controller -> Infrastructure -> Shared -> app
    app_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    docs_dir = os.path.join(app_dir, 'APIDocs')

    response = make_response(send_from_directory(docs_dir, 'apidoc.yaml'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/yaml'
    return response
