from typing import Optional, Union
from sqlalchemy import select, func
from Admin.Application.ReadModels.UserReadModel import UserReadModel
from Shared.Infrastructure.Persistence.database import db
from Admin.Domain.UserReadRepositoryInterface import UserReadRepositoryInterface
from Admin.Domain.User import User
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserReadRepository(UserReadRepositoryInterface):
    
    def find_by_id(
        self,
        id: Union[str, UuidValueObject],
    ) -> Optional[UserReadModel]:
        # Extraer el valor si es un ValueObject
        id_value = id.value if isinstance(id, UuidValueObject) else id
        stmt = select(UserModel).where(UserModel.id == id_value)
        model = db.session.execute(stmt).scalar_one_or_none()

        if model is None:
            return None

        return self._to_read_model(model)
    
    def _to_read_model(self, model: UserModel) -> UserReadModel:
        """
        Convierte un modelo SQLAlchemy a ReadModel.

        Args:
            model: Modelo de SQLAlchemy

        Returns:
            HelloWorldReadModel
        """
        return UserReadModel(
            id=model.id,
            username=model.username,
            email=model.email,
        )