from flask import Flask


def configureControllers(app: Flask):
    from Shared.Infrastructure.Controller.Controller import v1_controller_base
    from Shared.Infrastructure.Controller.ToolsController import tools_controller
    from Shared.Infrastructure.Controller.SwaggerController import swaggerui_blueprint, swagger_static
    from Admin.Infrastructure.Controller.AdminUserController import admin_user_controller
    from Admin2.controller import admin2_bp

    # Deshabilitar strict_slashes para evitar redirects 308
    app.url_map.strict_slashes = False

    app.register_blueprint(v1_controller_base, url_prefix='/api/v1')
    app.register_blueprint(admin_user_controller, url_prefix='/api/v1/admin/users')
    app.register_blueprint(tools_controller, url_prefix='/tools')
    app.register_blueprint(admin2_bp)

    # Registrar Swagger UI y endpoint para servir el spec
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(swagger_static)
