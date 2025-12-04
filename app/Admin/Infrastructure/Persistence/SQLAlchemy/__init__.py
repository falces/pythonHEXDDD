"""
Módulo de modelos SQLAlchemy para Admin.
Importar los modelos en orden para evitar problemas de dependencias.
"""
from Admin.Infrastructure.Persistence.SQLAlchemy.UserModel import UserModel
from Admin.Infrastructure.Persistence.SQLAlchemy.UserAddressModel import UserAddressModel

__all__ = ['UserModel', 'UserAddressModel']
