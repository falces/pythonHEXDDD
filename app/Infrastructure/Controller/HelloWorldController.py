from flask import Blueprint, request, current_app
from Infrastructure.Controller.ControllerBase import ControllerBase
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException


helloWorldController = Blueprint('helloWorldController', __name__)


class HelloWorldController:
    """
    Controlador para las operaciones de HelloWorld.
    Usa el DI Container para obtener casos de uso.
    """

    @helloWorldController.route('/', methods=['GET'])
    def getAllHelloWorld():
        """
        Obtiene todos los HelloWorld registrados.
        
        GET /api/v1/hello-world/
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.get_all_hello_world_use_case()
        
        # Ejecutar el caso de uso
        result = use_case.execute()
        
        return ControllerBase.formatResponse(result, 200)

    @helloWorldController.route('/', methods=['POST'])
    def createHelloWorld():
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
                return ControllerBase.formatResponse(
                    {"error": "Field 'name' is required"},
                    400
                )
            
            # Obtener caso de uso desde el container
            use_case = current_app.container.create_hello_world_use_case()
            
            # Ejecutar caso de uso con el texto del greeting
            result = use_case.execute(data['name'])
            
            return ControllerBase.formatResponse(result, 201)

        except IncorrectGreetingException as e:
            return ControllerBase.formatResponse({"error": str(e)}, 400)
            
        except Exception as e:
            return ControllerBase.formatResponse(
                {"error": str(e)},
                500
            )

    @helloWorldController.route('/<int:id>', methods=['GET'])
    def getHelloWorldById(id: int):
        """
        Obtiene un HelloWorld por su ID.
        
        GET /api/v1/hello-world/{id}
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.get_hello_world_by_id_use_case()
        
        # Ejecutar caso de uso
        result = use_case.execute(id)
        
        if result is None:
            return ControllerBase.formatResponse(
                {"error": "HelloWorld not found"},
                404
            )
        
        return ControllerBase.formatResponse(result, 200)

    @helloWorldController.route('/<int:id>', methods=['DELETE'])
    def deleteHelloWorld(id: int):
        """
        Elimina un HelloWorld por su ID.
        
        DELETE /api/v1/hello-world/{id}
        """
        # Obtener caso de uso desde el container
        use_case = current_app.container.delete_hello_world_use_case()
        
        # Ejecutar caso de uso
        deleted = use_case.execute(id)
        
        if not deleted:
            return ControllerBase.formatResponse(
                {"error": "HelloWorld not found"},
                404
            )
        
        return ControllerBase.formatResponse(
            {"message": "HelloWorld deleted successfully"},
            200
        )
