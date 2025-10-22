from Shared.Domain.Repositories.AbstractRepository import AbstractRepository
from Domain.HelloWorld import HelloWorld
from app import signals
import uuid
from Application.DTO import GreetingDTO
from Shared.Application.CreateExcelService import CreateExcelService


class MoviesService:
    def __init__(
        self,
        repository: AbstractRepository,
    ):
        self.repository = repository()

    def getMoviesByCriteria(
        self,
        args: dict = None,
        resultsInFile: bool = False,
        fileName: str = None,
    ) -> list:
        movies = self.repository.findByCriteria(
            args = args,
        )

        if resultsInFile:
            CreateExcelService.createExcelFromAPIResponse(movies.json(), fileName)
            
        return movies
    
    def addCountry(
        self,
        greetingDTO: GreetingDTO,
    ):
        greeting = HelloWorld(
            name = greetingDTO.name,
        )

        self.repository.save(greeting)

        signals['new_hello_world'].send(
            sender=uuid.uuid4().hex,
            message=greeting.toDict(),
        )