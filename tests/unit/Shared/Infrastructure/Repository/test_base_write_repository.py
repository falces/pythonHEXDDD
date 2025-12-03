"""
Tests unitarios para BaseWriteRepository.
Verifica el manejo centralizado de errores de base de datos.
"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from Shared.Infrastructure.Repository.BaseWriteRepository import BaseWriteRepository
from Shared.Infrastructure.Exceptions.DatabaseException import DatabaseException


class ConcreteWriteRepository(BaseWriteRepository[dict]):
    """
    Implementación concreta para testing.
    """
    pass


class TestBaseWriteRepository:
    """Tests para BaseWriteRepository."""
    
    @pytest.fixture
    def repository(self):
        """Fixture que proporciona una instancia del repositorio."""
        return ConcreteWriteRepository()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_success(self, mock_db, repository):
        """Verifica que las operaciones exitosas retornan el resultado."""
        expected_result = {"id": "123", "name": "test"}
        operation = MagicMock(return_value=expected_result)
        
        result = repository._execute(operation, {"entity": "Test"})
        
        assert result == expected_result
        operation.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_integrity_error(self, mock_db, repository):
        """Verifica que IntegrityError lanza DatabaseException con código 409."""
        mock_original = MagicMock()
        mock_original.errno = 1062
        mock_original.msg = "Duplicate entry"
        
        integrity_error = IntegrityError("statement", {}, mock_original)
        operation = MagicMock(side_effect=integrity_error)
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute(operation, {"entity": "User"})
        
        assert exc_info.value.code == 409
        assert "Integrity error" in str(exc_info.value)
        mock_db.session.rollback.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_operational_error(self, mock_db, repository):
        """Verifica que OperationalError lanza DatabaseException con código 503."""
        mock_original = MagicMock()
        mock_original.errno = 2003
        mock_original.msg = "Can't connect to MySQL server"
        
        operational_error = OperationalError("statement", {}, mock_original)
        operation = MagicMock(side_effect=operational_error)
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute(operation, {"entity": "User"})
        
        assert exc_info.value.code == 503
        assert "connection error" in str(exc_info.value)
        mock_db.session.rollback.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_sqlalchemy_error(self, mock_db, repository):
        """Verifica que SQLAlchemyError lanza DatabaseException con código 500."""
        sqlalchemy_error = SQLAlchemyError("Generic SQLAlchemy error")
        operation = MagicMock(side_effect=sqlalchemy_error)
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute(operation, {"entity": "User"})
        
        assert exc_info.value.code == 500
        assert "Database error" in str(exc_info.value)
        mock_db.session.rollback.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_unexpected_error(self, mock_db, repository):
        """Verifica que excepciones inesperadas lanzan DatabaseException con código 500."""
        operation = MagicMock(side_effect=ValueError("Unexpected error"))
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute(operation, {"entity": "User"})
        
        assert exc_info.value.code == 500
        assert "Unexpected error" in str(exc_info.value)
        mock_db.session.rollback.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_always_closes_session(self, mock_db, repository):
        """Verifica que la sesión siempre se cierra, incluso con error."""
        operation = MagicMock(side_effect=IntegrityError("statement", {}, Exception("test")))
        
        with pytest.raises(DatabaseException):
            repository._execute(operation, {"entity": "User"})
        
        mock_db.session.close.assert_called_once()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    def test_execute_closes_session_on_success(self, mock_db, repository):
        """Verifica que la sesión se cierra en operaciones exitosas."""
        operation = MagicMock(return_value={"id": "123"})
        
        repository._execute(operation, {"entity": "User"})
        
        mock_db.session.close.assert_called_once()


class TestExtractMySQLErrorCode:
    """Tests para _extract_mysql_error."""
    
    @pytest.fixture
    def repository(self):
        return ConcreteWriteRepository()
    
    def test_extract_mysql_error_with_errno(self, repository):
        """Extrae errno del error original de MySQL."""
        mock_original = MagicMock()
        mock_original.errno = 1062
        mock_original.msg = "Duplicate entry"
        
        error = IntegrityError("statement", {}, mock_original)
        
        result = repository._extract_mysql_error(error)
        
        assert result["code"] == 1062
        assert result["message"] == "Duplicate entry"
    
    def test_extract_mysql_error_with_args(self, repository):
        """Extrae código de args cuando errno no existe."""
        mock_original = MagicMock(spec=[])  # Sin errno
        mock_original.args = [2003, "Can't connect"]
        
        error = OperationalError("statement", {}, mock_original)
        
        result = repository._extract_mysql_error(error)
        
        assert result["code"] == 2003
    
    def test_extract_mysql_error_without_orig(self, repository):
        """Retorna None para código cuando no hay error original."""
        error = SQLAlchemyError("Generic error")
        
        result = repository._extract_mysql_error(error)
        
        assert result["code"] is None
        assert "Generic error" in result["message"]


class TestLogging:
    """Tests para verificar el logging."""
    
    @pytest.fixture
    def repository(self):
        return ConcreteWriteRepository()
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.logger')
    def test_logs_integrity_error(self, mock_logger, mock_db, repository):
        """Verifica que los errores de integridad se loguean correctamente."""
        mock_original = MagicMock()
        mock_original.errno = 1062
        mock_original.msg = "Duplicate entry 'test@email.com'"
        
        error = IntegrityError("statement", {}, mock_original)
        operation = MagicMock(side_effect=error)
        context = {"entity": "User", "email": "test@email.com"}
        
        with pytest.raises(DatabaseException):
            repository._execute(operation, context)
        
        mock_logger.error.assert_called_once()
        log_message = mock_logger.error.call_args[0][0]
        assert "IntegrityError" in log_message
        assert "1062" in log_message
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.logger')
    def test_logs_operational_error(self, mock_logger, mock_db, repository):
        """Verifica que los errores operacionales se loguean correctamente."""
        mock_original = MagicMock()
        mock_original.errno = 2003
        mock_original.msg = "Can't connect to MySQL server"
        
        error = OperationalError("statement", {}, mock_original)
        operation = MagicMock(side_effect=error)
        context = {"entity": "User"}
        
        with pytest.raises(DatabaseException):
            repository._execute(operation, context)
        
        mock_logger.error.assert_called_once()
        log_message = mock_logger.error.call_args[0][0]
        assert "OperationalError" in log_message
    
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.db')
    @patch('Shared.Infrastructure.Repository.BaseWriteRepository.logger')
    def test_logs_context(self, mock_logger, mock_db, repository):
        """Verifica que el contexto se incluye en el log."""
        error = SQLAlchemyError("Generic error")
        operation = MagicMock(side_effect=error)
        context = {"entity": "User", "operation": "save", "username": "john"}
        
        with pytest.raises(DatabaseException):
            repository._execute(operation, context)
        
        log_message = mock_logger.error.call_args[0][0]
        assert "User" in log_message
        assert "save" in log_message
        assert "john" in log_message
