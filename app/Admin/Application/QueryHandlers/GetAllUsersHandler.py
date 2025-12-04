from typing import List
from Shared.Application.QueryHandler import QueryHandler
from Admin.Domain.Repository.UserReadRepositoryInterface import UserReadRepositoryInterface
from Admin.Application.Queries.GetAllUsersQuery import GetAllUsersQuery
from Admin.Application.ReadModels.UserReadModel import UserReadModel


class GetAllUsersHandler(QueryHandler):
    """Handler para obtener todos los usuarios."""
    
    def __init__(self, read_repository: UserReadRepositoryInterface):
        self.read_repository = read_repository
        
    def handle(self, query: GetAllUsersQuery) -> List[dict]:
        users = self.read_repository.find_all()
        return [user.to_dict() for user in users]
