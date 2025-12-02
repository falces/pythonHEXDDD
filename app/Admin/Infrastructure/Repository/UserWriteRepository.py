from Shared.Infrastructure.Persistence.database import db
from Admin.Domain.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Admin.Domain.User import User
from Admin.Infrastructure.Persistence.Mappers.UserMapper import UserMapper


class UserWriteRepository(UserWriteRepositoryInterface):
    
    def save(
        self,
        user: User,
    ):
        
        model = UserMapper.toModel(user)
        
        merged_model = db.session.merge(model)
        db.session.commit()
        db.session.refresh(merged_model)
        
        return UserMapper.toDomain(merged_model)