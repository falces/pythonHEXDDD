from typing import Optional, Union
from sqlalchemy import select
from Admin.Application.ReadModels.UserReadModel import UserReadModel
from Shared.Infrastructure.Persistence.database import db
from Admin.Domain.Repository.UserReadRepositoryInterface import UserReadRepositoryInterface
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserReadRepository(UserReadRepositoryInterface):
    
    def find_by_id(
        self,
        id: Union[str, UuidValueObject],
    ) -> Optional[UserReadModel]:
        id_value = id.value if isinstance(id, UuidValueObject) else id
        stmt = select(UserModel).where(UserModel.id == id_value)
        model = db.session.execute(stmt).scalar_one_or_none()

        if model is None:
            return None

        return self._to_read_model(model)
    
    def _to_read_model(self, model: UserModel) -> UserReadModel:
        return UserReadModel(
            id=model.id,
            username=model.username,
            email=model.email,
        )