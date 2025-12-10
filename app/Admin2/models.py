"""
Modelos SQLAlchemy para Admin2.
Arquitectura simple sin DDD/CQRS/Hexagonal.
"""
import uuid
from Shared.Infrastructure.Persistence.database import db
from sqlalchemy import Column, String


class User(db.Model):
    """Modelo de usuario."""
    
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    def __init__(self, username: str, email: str, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.username = username
        self.email = email
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
