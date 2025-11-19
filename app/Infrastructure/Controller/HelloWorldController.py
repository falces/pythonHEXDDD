from flask import Blueprint, request, current_app
from Infrastructure.Controller.ControllerBase import ControllerBase
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException


hello_world_controller = Blueprint('helloWorldController', __name__)


class HelloWorldController:
    """
    Controlador para las operaciones de HelloWorld.
    Usa el DI Container para obtener casos de uso.
    """

    @hello_world_controller.route('/', methods=['GET'])
    def get_all_hello_world():
        """
        Obtiene todos los HelloWorld registrados.
        
        GET /api/v1/hello-world/
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.get_all_hello_world_use_case()
        
        # Ejecutar el caso de uso
        result = use_case.execute()
        
        return ControllerBase.format_response(result, 200)

    @hello_world_controller.route('/', methods=['POST'])
    def create_hello_world():
        """
        Crea un nuevo HelloWorld.
        
        POST /api/v1/hello-world/
        Body: {
            "name": "Hello from Spain"
        }
        """
        try:
            # Obtener datos del request
            data = request.get_json()
            
            if not data or 'name' not in data:
                return ControllerBase.format_response(
                    {"error": "Field 'name' is required"},
                    400
                )
            
            # Obtener caso de uso desde el container
            use_case = current_app.container.create_hello_world_use_case()
            
            # Ejecutar caso de uso con el texto del greeting
            result = use_case.execute(data['name'])
            
            return ControllerBase.format_response(result, 201)

        except IncorrectGreetingException as e:
            return ControllerBase.format_response({"error": str(e)}, 400)
            
        except Exception as e:
            return ControllerBase.format_response(
                {"error": str(e)},
                500
            )

    @hello_world_controller.route('/<int:id>', methods=['GET'])
    def get_hello_world_by_id(id: int):
        """
        Obtiene un HelloWorld por su ID.
        
        GET /api/v1/hello-world/{id}
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.get_hello_world_by_id_use_case()
        
        # Ejecutar caso de uso
        result = use_case.execute(id)
        
        if result is None:
            return ControllerBase.format_response(
                {"error": "HelloWorld not found"},
                404
            )
        
        return ControllerBase.format_response(result, 200)

    @hello_world_controller.route('/<int:id>', methods=['DELETE'])
    def delete_hello_world(id: int):
        """
        Elimina un HelloWorld por su ID.
        
        DELETE /api/v1/hello-world/{id}
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.delete_hello_world_use_case()
        
        # Ejecutar caso de uso
        deleted = use_case.execute(id)
        
        if not deleted:
            return ControllerBase.format_response(
                {"error": "HelloWorld not found"},
                404
            )
        
        return ControllerBase.format_response(
            {"message": "HelloWorld deleted successfully"},
            200
        )
