"""
Mapper para la entidad UserAddress.
Convierte entre dominio e infraestructura.
"""
from Admin.Domain.Entities.UserAddress import UserAddress
from Admin.Infrastructure.Persistence.SQLAlchemy.UserAddressModel import UserAddressModel
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserAddressMapper:

    @staticmethod
    def toDomain(model: UserAddressModel) -> UserAddress:
        """Convierte un modelo de persistencia a entidad de dominio."""
        if model is None:
            return None

        return UserAddress(
            id=UuidValueObject.create(model.id),
            street=model.street,
            city=model.city,
            country=model.country,
        )
    
    @staticmethod
    def toModel(address: UserAddress, user_id: str) -> UserAddressModel:
        """Convierte una entidad de dominio a modelo de persistencia."""
        if address is None:
            return None
            
        return UserAddressModel(
            id=address.id.value,
            user_id=user_id,
            street=address.street,
            city=address.city,
            country=address.country,
        )
    
    @staticmethod
    def toDomainList(models: list[UserAddressModel]) -> list[UserAddress]:
        """Convierte una lista de modelos a entidades de dominio."""
        return [UserAddressMapper.toDomain(m) for m in models] if models else []
    
    @staticmethod
    def toModelList(addresses: list[UserAddress], user_id: str) -> list[UserAddressModel]:
        """Convierte una lista de entidades a modelos de persistencia."""
        return [UserAddressMapper.toModel(a, user_id) for a in addresses] if addresses else []
