from Shared.Infrastructure.Persistence.database import db
from Shared.Infrastructure.Repository.BaseWriteRepository import BaseWriteRepository
from Admin.Domain.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Admin.Domain.User import User
from Admin.Infrastructure.Persistence.Mappers.UserMapper import UserMapper


class UserWriteRepository(BaseWriteRepository[User], UserWriteRepositoryInterface):
    """
    Implementación del repositorio de escritura de usuarios.
    Extiende BaseWriteRepository para heredar el manejo centralizado de errores de BD.
    """
    
    def save(self, user: User) -> User:
        """
        Persiste un usuario en la base de datos.
        
        Args:
            user: Entidad User a persistir
            
        Returns:
            User: Entidad User persistida
            
        Raises:
            DatabaseException: Si ocurre un error de base de datos
        """
        def save_operation():
            model = UserMapper.toModel(user)
            merged_model = db.session.merge(model)
            db.session.commit()
            db.session.refresh(merged_model)
            return UserMapper.toDomain(merged_model)
        
        context = {
            'entity': 'User',
            'operation': 'save',
            'username': user.username.value,
            'email': user.email.value
        }
        
        return self._execute(save_operation, context)