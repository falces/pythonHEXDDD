from flask import Blueprint, request, current_app
from Infrastructure.Controller.ControllerBase import ControllerBase


moviesController = Blueprint('moviesController', __name__)


class MoviesController:
    """
    Controlador para las operaciones de Shows/Movies.
    Usa el DI Container para obtener casos de uso.
    """

    @moviesController.route('/', methods=['GET'])
    def getMoviesBy():
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
        
        return ControllerBase.formatResponse(result, 200)

    @moviesController.route('/<string:show_id>', methods=['GET'])
    def getMovieById(show_id: str):
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
            return ControllerBase.formatResponse(
                {"error": "Show not found"},
                404
            )
        
        return ControllerBase.formatResponse(result, 200)