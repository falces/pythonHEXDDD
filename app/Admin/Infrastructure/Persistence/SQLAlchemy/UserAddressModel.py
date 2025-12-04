"""
Modelo SQLAlchemy para UserAddress.
Representa la tabla de direcciones de usuarios.
"""
from Shared.Infrastructure.Persistence.database import db
from sqlalchemy import Column, String, ForeignKey


class UserAddressModel(db.Model):
    
    __tablename__ = 'user_addresses'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    
    def __init__(
        self,
        id: str,
        user_id: str,
        street: str,
        city: str,
        country: str,
    ):
        self.id = id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.country = country
