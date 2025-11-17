from flask import Flask


def configureControllers(app: Flask):
    from Shared.Infrastructure.Controller.Controller import v1ControllerBase
    from Shared.Infrastructure.Controller.ToolsController import toolsController
    from Shared.Infrastructure.Controller.SwaggerController import swaggerui_blueprint, swagger_static
    
    app.register_blueprint(v1ControllerBase, url_prefix='/api/v1')
    app.register_blueprint(toolsController, url_prefix='/tools')
    
    # Registrar Swagger UI y endpoint para servir el spec
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(swagger_static)