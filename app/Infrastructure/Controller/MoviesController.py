from flask import Blueprint, request, current_app
from Infrastructure.Controller.ControllerBase import ControllerBase


movies_controller = Blueprint('moviesController', __name__)


class MoviesController:
    """
    Controlador para las operaciones de Shows/Movies.
    Usa el DI Container para obtener casos de uso.
    """

    @movies_controller.route('/', methods=['GET'])
    def get_movies_by():
        """
        Obtiene shows/movies según criterios de búsqueda.
        
        GET /api/v1/movies/?country=us&showType=movie
        """
        # Obtener caso de uso desde el container
        container = current_app.container
        use_case = container.search_shows_use_case()
        
        # Convertir request.args (ImmutableMultiDict) a dict normal
        criteria = request.args.to_dict()
        
        # Ejecutar el caso de uso
        result = use_case.execute(criteria)
        
        return ControllerBase.format_response(result, 200)

    @movies_controller.route('/<string:show_id>', methods=['GET'])
    def get_movie_by_id(show_id: str):
        """
        Obtiene un show/movie por su ID.
        
        GET /api/v1/movies/{show_id}
        """
        # Obtener caso de uso desde el container
        container = current_app.container
        use_case = container.get_show_by_id_use_case()
        
        # Ejecutar caso de uso
        result = use_case.execute(show_id)
        
        if result is None:
            return ControllerBase.format_response(
                {"error": "Show not found"},
                404
            )
        
        return ControllerBase.format_response(result, 200)