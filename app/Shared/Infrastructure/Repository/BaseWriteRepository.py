"""
Clase base para repositorios de escritura.
Centraliza el manejo de errores de base de datos y logging.
"""

from typing import TypeVar, Callable, Any, Generic
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from config.log import logger
from Shared.Infrastructure.Exceptions.DatabaseException import DatabaseException
from Shared.Infrastructure.Persistence.database import db

T = TypeVar('T')


class BaseWriteRepository(Generic[T]):
    """
    Clase base para repositorios de escritura.
    
    Proporciona manejo centralizado de:
    - Errores de base de datos (IntegrityError, OperationalError, etc.)
    - Logging de errores
    - Rollback automático en caso de error
    - Cierre de sesión en finally
    
    Ejemplo de uso:
        class UserWriteRepository(BaseWriteRepository, UserWriteRepositoryInterface):
            def save(self, user: User) -> User:
                def operation():
                    model = UserMapper.toModel(user)
                    merged = db.session.merge(model)
                    db.session.commit()
                    db.session.refresh(merged)
                    return UserMapper.toDomain(merged)
                
                return self._execute(operation, context={"user": user.username.value})
    """
    
    def _execute(
        self,
        operation: Callable[[], T],
        context: dict = None
    ) -> T:
        """
        Ejecuta una operación de base de datos con manejo de errores centralizado.
        
        Args:
            operation: Función que contiene la lógica de base de datos
            context: Diccionario con información de contexto para logging
            
        Returns:
            El resultado de la operación
            
        Raises:
            DatabaseException: En caso de error de base de datos
        """
        context = context or {}
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        
        try:
            with db.session.begin():
                return operation()
        
        except IntegrityError as e:
            db.session.rollback()
            mysql_error = self._extract_mysql_error(e)
            logger.error(
                f"[MySQL IntegrityError] Code: {mysql_error['code']}, "
                f"Message: {mysql_error['message']}"
                + (f", Context: {context_str}" if context_str else "")
            )
            raise DatabaseException(
                message=f"Integrity error: {mysql_error['message']}",
                code=409  # Conflict
            )
        
        except OperationalError as e:
            db.session.rollback()
            mysql_error = self._extract_mysql_error(e)
            logger.error(
                f"[MySQL OperationalError] Code: {mysql_error['code']}, "
                f"Message: {mysql_error['message']}"
                + (f", Context: {context_str}" if context_str else "")
            )
            raise DatabaseException(
                message=f"Database connection error: {mysql_error['message']}",
                code=503  # Service Unavailable
            )
        
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(
                f"[SQLAlchemy Error] {type(e).__name__}: {str(e)}"
                + (f", Context: {context_str}" if context_str else "")
            )
            raise DatabaseException(
                message=f"Database error: {str(e)}",
                code=500
            )
        
        except Exception as e:
            db.session.rollback()
            logger.error(
                f"[Unexpected Error] {type(e).__name__}: {str(e)}"
                + (f", Context: {context_str}" if context_str else "")
            )
            raise DatabaseException(
                message=f"Unexpected error: {str(e)}",
                code=500
            )
        
        finally:
            db.session.close()
    
    def _extract_mysql_error(self, exception: Exception) -> dict:
        """
        Extrae el código y mensaje de error de MySQL desde la excepción.
        
        Args:
            exception: Excepción de SQLAlchemy
            
        Returns:
            Diccionario con 'code' y 'message'
        """
        original = getattr(exception, 'orig', None)
        
        if original is not None:
            # MySQL Connector error
            code = getattr(original, 'errno', None)
            if code is None and hasattr(original, 'args') and len(original.args) > 0:
                code = original.args[0]
            message = getattr(original, 'msg', None) or str(original)
        else:
            code = None
            message = str(exception)
        
        return {
            'code': code,
            'message': message
        }
