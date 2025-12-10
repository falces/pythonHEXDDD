from Admin.Domain.User import User
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Admin.Infrastructure.Persistence.Mappers.UserAddressMapper import UserAddressMapper
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserMapper:

    @staticmethod
    def toDomain(model: UserModel, address_models: list = None) -> User:
        """
        Convierte un modelo de persistencia a entidad de dominio.
        
        Args:
            model: Modelo UserModel de SQLAlchemy
            address_models: Lista opcional de UserAddressModel
        """
        if model is None:
            return None

        username = UsernameValueObject.create(model.username)
        email = EmailValueObject.create(model.email)
        id = UuidValueObject.create(model.id)
        
        # Mapear direcciones si se proporcionan
        addresses = []
        if address_models:
            addresses = UserAddressMapper.toDomainList(address_models)
        
        user = User(
            username=username,
            email=email,
            id=id,
            addresses=addresses,
        )
        
        return user
    
    @staticmethod
    def toModel(user: User) -> UserModel:
        if user is None:
            return None
            
        model = UserModel(
            username=user.username.value,
            email=user.email.value,
            id=user.id.value,
        )
        
        return model
        