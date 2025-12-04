from typing import Optional, Union, List
from sqlalchemy import select
from Admin.Application.ReadModels.UserReadModel import UserReadModel
from Shared.Infrastructure.Persistence.database import db
from Admin.Domain.Repository.UserReadRepositoryInterface import UserReadRepositoryInterface
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Admin.Infrastructure.Persistence.SQLAlchemy.UserAddressModel import UserAddressModel
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

        # Cargar direcciones por separado
        address_models = db.session.query(UserAddressModel).filter_by(
            user_id=id_value
        ).all()

        return self._to_read_model(model, address_models)
    
    def find_all(self) -> List[UserReadModel]:
        """Obtiene todos los usuarios."""
        stmt = select(UserModel).order_by(UserModel.username)
        models = db.session.execute(stmt).scalars().all()
        
        result = []
        for model in models:
            address_models = db.session.query(UserAddressModel).filter_by(
                user_id=model.id
            ).all()
            result.append(self._to_read_model(model, address_models))
        
        return result
    
    def _to_read_model(self, model: UserModel, address_models: list) -> UserReadModel:
        addresses = [
            {
                "id": addr.id,
                "street": addr.street,
                "city": addr.city,
                "country": addr.country,
            }
            for addr in address_models
        ]
        return UserReadModel(
            id=model.id,
            username=model.username,
            email=model.email,
            addresses=addresses,
        )