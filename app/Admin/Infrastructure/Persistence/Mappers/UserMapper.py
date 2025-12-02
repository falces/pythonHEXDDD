from Admin.Domain.User import User
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserMapper:

    @staticmethod
    def toDomain(model: UserModel) -> User:
        if model is None:
            return None

        username = UsernameValueObject.create(model.username)
        email = EmailValueObject.create(model.email)
        id = UuidValueObject.create(model.id)
        
        user = User.create(
            username=username,
            email=email,
            id=id,
            )
        
        return user
    
    @staticmethod
    def toModel(user: User) -> UserModel:
        
        if user is None:
            return None
        return UserModel(
            username=user.username.value,
            email=user.email.value,
            id=user.id.value,
        )
        