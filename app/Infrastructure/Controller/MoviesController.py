from flask import Blueprint, request
# from Application.HelloWorldService import HelloWorldService
from Application.MoviesService import MoviesService
from Infrastructure.Repository.ShowsRepository import ShowsRepository
from Infrastructure.Controller.ControllerBase import ControllerBase
from flask import current_app as app


moviesController = Blueprint('moviesController', __name__)

class MoviesController():

    @moviesController.route('/', methods=['GET'])
    def getMoviesBy():
        app.logger.info("Query String: " + str(request.query_string))
        
        moviesService = MoviesService(ShowsRepository)

        return ControllerBase.formatResponse(
            moviesService.getMoviesByCriteria(request.args),
            200,
        )