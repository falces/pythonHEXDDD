from Shared.Infrastructure.Persistence.database import db
from sqlalchemy import Column, String


class UserModel(db.Model):
    
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, nullable=False)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    
    def __init__(
        self,
        username: str,
        email: str,
        id: str = None
    ):
        self.id = id
        self.username = username
        self.email = email
