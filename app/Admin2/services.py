"""
Servicios para Admin2.
Contiene la lógica de negocio de usuarios.
"""
from typing import Optional
from sqlalchemy.exc import IntegrityError
from Shared.Infrastructure.Persistence.database import db
from Admin2.models import User


class UserService:
    """Servicio para gestión de usuarios."""
    
    def create(self, username: str, email: str) -> User:
        """
        Crea un nuevo usuario.
        
        Raises:
            ValueError: Si el usuario ya existe
        """
        try:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por ID."""
        return db.session.get(User, user_id)
    
    def get_all(self) -> list[User]:
        """Obtiene todos los usuarios."""
        return db.session.query(User).all()
    
    def update(self, user_id: str, username: str = None, email: str = None) -> Optional[User]:
        """
        Actualiza un usuario existente.
        
        Returns:
            User actualizado o None si no existe
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        try:
            if username:
                user.username = username
            if email:
                user.email = email
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")
    
    def delete(self, user_id: str) -> bool:
        """
        Elimina un usuario.
        
        Returns:
            True si se eliminó, False si no existía
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
