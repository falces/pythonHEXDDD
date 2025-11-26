from flask import Blueprint, request, current_app
from Infrastructure.Controller.ControllerBase import ControllerBase
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery


hello_world_controller = Blueprint('helloWorldController', __name__)


class HelloWorldController:
    """
    Controlador para las operaciones de HelloWorld.
    Usa CQRS puro: CommandBus para escrituras, QueryBus para lecturas.
    """

    @hello_world_controller.route('/', methods=['GET'])
    def get_all_hello_world():
        """
        Obtiene todos los HelloWorld registrados.

        GET /api/v1/hello-world/
        Query params: limit, offset, sort_by, sort_order
        """
        # Obtener parámetros de paginación/ordenamiento
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        sort_by = request.args.get('sort_by', default='id')
        sort_order = request.args.get('sort_order', default='asc')

        # Crear Query
        query = GetAllHelloWorldQuery(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )

        # Obtener QueryBus y despachar
        query_bus = current_app.container.query_bus()
        result = query_bus.dispatch(query)

        return ControllerBase.format_response(result, 200)

    @hello_world_controller.route('/', methods=['POST'])
    def create_hello_world():
        """
        Crea un nuevo HelloWorld usando CQRS.

        POST /api/v1/hello-world/
        Body: {
            "greeting": "Hello from Spain"
        }
        """
        try:
            # Obtener datos del request
            data = request.get_json()

            if not data or 'greeting' not in data:
                return ControllerBase.format_response(
                    {"error": "Field 'greeting' is required"},
                    400
                )

            # Crear el comando CQRS
            command = CreateHelloWorldCommand(
                greeting_text=data['greeting']
            )

            # Obtener el Command Bus y despachar
            command_bus = current_app.container.command_bus()
            entity_id = command_bus.dispatch(command)

            # Usar QueryBus para obtener la entidad creada
            query = GetHelloWorldByIdQuery(id=entity_id)
            query_bus = current_app.container.query_bus()
            created_entity = query_bus.dispatch(query)

            return ControllerBase.format_response(
                created_entity,
                201
            )

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
        # Crear Query
        query = GetHelloWorldByIdQuery(id=id)

        # Obtener QueryBus y despachar
        query_bus = current_app.container.query_bus()
        result = query_bus.dispatch(query)

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
        # Verificar que existe antes de eliminar
        query = GetHelloWorldByIdQuery(id=id)
        query_bus = current_app.container.query_bus()
        existing = query_bus.dispatch(query)

        if existing is None:
            return ControllerBase.format_response(
                {"error": "HelloWorld not found"},
                404
            )

        # Crear Comando y despachar
        command = DeleteHelloWorldCommand(id=id)
        command_bus = current_app.container.command_bus()
        command_bus.dispatch(command)

        return ControllerBase.format_response(
            {"message": "HelloWorld deleted successfully"},
            200
        )
