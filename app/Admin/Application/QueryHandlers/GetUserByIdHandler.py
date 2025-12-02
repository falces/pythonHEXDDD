from typing import Optional
from Shared.Application.QueryHandler import QueryHandler
from Admin.Domain.UserReadRepositoryInterface import UserReadRepositoryInterface
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery
from Admin.Application.ReadModels.UserReadModel import UserReadModel


class GetUserByIdHandler(QueryHandler):
    
    def __init__(
        self,
        read_repository: UserReadRepositoryInterface,
    ):
        self.read_repository = read_repository
        
    def handle(
        self,
        query: GetUserByIdQuery,
    ) -> Optional[dict]:
        user_model = self.read_repository.find_by_id(query.id)
        
        if user_model is None:
            return None
        
        return user_model.to_dict()
        