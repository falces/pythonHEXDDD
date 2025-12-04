from typing import Optional
from Shared.Infrastructure.Persistence.database import db
from Shared.Infrastructure.Repository.BaseWriteRepository import BaseWriteRepository
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Admin.Domain.User import User
from Admin.Infrastructure.Persistence.Mappers.UserMapper import UserMapper
from Admin.Infrastructure.Persistence.Mappers.UserAddressMapper import UserAddressMapper
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Admin.Infrastructure.Persistence.SQLAlchemy.UserAddressModel import UserAddressModel


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
            # Guardar usuario
            model = UserMapper.toModel(user)
            merged_model = db.session.merge(model)
            
            # Obtener direcciones actuales en BD
            existing_addresses = db.session.query(UserAddressModel).filter_by(
                user_id=user.id.value
            ).all()
            existing_ids = {addr.id for addr in existing_addresses}
            
            # IDs de direcciones en el dominio
            domain_ids = {addr.id.value for addr in user.addresses}
            
            # Eliminar direcciones que ya no existen en el dominio
            for addr in existing_addresses:
                if addr.id not in domain_ids:
                    db.session.delete(addr)
            
            # Añadir o actualizar direcciones del dominio
            for address in user.addresses:
                address_model = UserAddressMapper.toModel(address, user.id.value)
                db.session.merge(address_model)
            
            db.session.commit()
            db.session.refresh(merged_model)
            
            # Recargar direcciones
            address_models = db.session.query(UserAddressModel).filter_by(
                user_id=user.id.value
            ).all()
            
            return UserMapper.toDomain(merged_model, address_models)
        
        context = {
            'entity': 'User',
            'operation': 'save',
            'username': user.username.value,
            'email': user.email.value
        }
        
        return self._execute(save_operation, context)
    
    def find_by_id(self, id: str) -> Optional[User]:
        """
        Busca un usuario por ID para operaciones de escritura.
        
        Args:
            id: ID del usuario
            
        Returns:
            User o None si no existe
        """
        def find_operation():
            model = db.session.get(UserModel, id)
            if not model:
                return None
            
            # Cargar direcciones
            address_models = db.session.query(UserAddressModel).filter_by(
                user_id=id
            ).all()
            
            return UserMapper.toDomain(model, address_models)
        
        context = {
            'entity': 'User',
            'operation': 'find_by_id',
            'id': id
        }
        
        return self._execute(find_operation, context)
    
    def delete(self, id: str) -> bool:
        """
        Elimina un usuario por ID.
        
        Args:
            id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            DatabaseException: Si ocurre un error de base de datos
        """
        def delete_operation():
            # Eliminar direcciones primero (o dejar que CASCADE lo haga)
            db.session.query(UserAddressModel).filter_by(user_id=id).delete()
            
            model = db.session.get(UserModel, id)
            if model:
                db.session.delete(model)
                db.session.commit()
                return True
            return False
        
        context = {
            'entity': 'User',
            'operation': 'delete',
            'id': id
        }
        
        return self._execute(delete_operation, context)