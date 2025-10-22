from flask import Flask


def configureControllers(app: Flask):
    from Shared.Infrastructure.Controller.Controller import v1ControllerBase
    from Shared.Infrastructure.Controller.ToolsController import toolsController
    
    app.register_blueprint(v1ControllerBase, url_prefix='/api/v1')
    app.register_blueprint(toolsController, url_prefix='/tools')