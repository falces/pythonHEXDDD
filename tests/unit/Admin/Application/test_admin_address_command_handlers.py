"""
Tests unitarios para los Command Handlers de UserAddress.
"""

import pytest
from unittest.mock import MagicMock, Mock
from Admin.Application.CommandHandlers.AddUserAddressHandler import AddUserAddressHandler
from Admin.Application.CommandHandlers.UpdateUserAddressHandler import UpdateUserAddressHandler
from Admin.Application.CommandHandlers.RemoveUserAddressHandler import RemoveUserAddressHandler
from Admin.Application.Commands.AddUserAddressCommand import AddUserAddressCommand
from Admin.Application.Commands.UpdateUserAddressCommand import UpdateUserAddressCommand
from Admin.Application.Commands.RemoveUserAddressCommand import RemoveUserAddressCommand
from Admin.Domain.User import User
from Admin.Domain.Entities.UserAddress import UserAddress
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class TestAddUserAddressHandler:
    """Tests para AddUserAddressHandler."""
    
    @pytest.fixture
    def mock_write_repository(self):
        return MagicMock()
    
    @pytest.fixture
    def mock_event_dispatcher(self):
        return MagicMock()
    
    @pytest.fixture
    def handler(self, mock_write_repository, mock_event_dispatcher):
        return AddUserAddressHandler(
            write_repository=mock_write_repository,
            event_dispatcher=mock_event_dispatcher
        )
    
    @pytest.fixture
    def sample_user(self):
        return User.create(
            id=UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000"),
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
    
    def test_add_address_successfully(self, handler, mock_write_repository, mock_event_dispatcher, sample_user):
        """Debería añadir dirección exitosamente."""
        mock_write_repository.find_by_id.return_value = sample_user
        mock_write_repository.save.return_value = sample_user
        
        command = AddUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        
        result = handler.handle(command)
        
        assert result is not None
        assert len(result) == 36  # UUID length
        mock_write_repository.find_by_id.assert_called_once_with("550e8400-e29b-41d4-a716-446655440000")
        mock_write_repository.save.assert_called_once()
    
    def test_add_address_user_not_found(self, handler, mock_write_repository):
        """Debería lanzar error si el usuario no existe."""
        mock_write_repository.find_by_id.return_value = None
        
        command = AddUserAddressCommand(
            user_id="nonexistent-id-00000000000000000",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        
        with pytest.raises(ValueError) as exc_info:
            handler.handle(command)
        
        assert "not found" in str(exc_info.value)
    
    def test_add_address_publishes_events(self, handler, mock_write_repository, mock_event_dispatcher, sample_user):
        """Debería publicar eventos de dominio."""
        mock_write_repository.find_by_id.return_value = sample_user
        mock_write_repository.save.return_value = sample_user
        
        command = AddUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        
        handler.handle(command)
        
        mock_event_dispatcher.publish_multiple.assert_called_once()


class TestUpdateUserAddressHandler:
    """Tests para UpdateUserAddressHandler."""
    
    @pytest.fixture
    def mock_write_repository(self):
        return MagicMock()
    
    @pytest.fixture
    def mock_event_dispatcher(self):
        return MagicMock()
    
    @pytest.fixture
    def handler(self, mock_write_repository, mock_event_dispatcher):
        return UpdateUserAddressHandler(
            write_repository=mock_write_repository,
            event_dispatcher=mock_event_dispatcher
        )
    
    @pytest.fixture
    def sample_user_with_address(self):
        user = User.create(
            id=UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000"),
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
        # Añadir dirección y limpiar eventos
        address = user.add_address("123 Main St", "New York", "USA")
        user.pull_domain_events()  # Limpiar eventos
        return user, address
    
    def test_update_address_successfully(self, handler, mock_write_repository, sample_user_with_address):
        """Debería actualizar dirección exitosamente."""
        user, address = sample_user_with_address
        mock_write_repository.find_by_id.return_value = user
        mock_write_repository.save.return_value = user
        
        command = UpdateUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id=address.id.value,
            street="456 Updated St"
        )
        
        result = handler.handle(command)
        
        assert result == address.id.value
        mock_write_repository.save.assert_called_once()
    
    def test_update_address_user_not_found(self, handler, mock_write_repository):
        """Debería lanzar error si el usuario no existe."""
        mock_write_repository.find_by_id.return_value = None
        
        command = UpdateUserAddressCommand(
            user_id="nonexistent-id-00000000000000000",
            address_id="660e8400-e29b-41d4-a716-446655440001",
            street="456 Updated St"
        )
        
        with pytest.raises(ValueError) as exc_info:
            handler.handle(command)
        
        assert "User" in str(exc_info.value)
        assert "not found" in str(exc_info.value)
    
    def test_update_address_address_not_found(self, handler, mock_write_repository):
        """Debería lanzar error si la dirección no existe."""
        user = User.create(
            id=UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000"),
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
        mock_write_repository.find_by_id.return_value = user
        
        command = UpdateUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001",
            street="456 Updated St"
        )
        
        with pytest.raises(ValueError) as exc_info:
            handler.handle(command)
        
        assert "Address" in str(exc_info.value)
        assert "not found" in str(exc_info.value)


class TestRemoveUserAddressHandler:
    """Tests para RemoveUserAddressHandler."""
    
    @pytest.fixture
    def mock_write_repository(self):
        return MagicMock()
    
    @pytest.fixture
    def mock_event_dispatcher(self):
        return MagicMock()
    
    @pytest.fixture
    def handler(self, mock_write_repository, mock_event_dispatcher):
        return RemoveUserAddressHandler(
            write_repository=mock_write_repository,
            event_dispatcher=mock_event_dispatcher
        )
    
    @pytest.fixture
    def sample_user_with_address(self):
        user = User.create(
            id=UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000"),
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
        address = user.add_address("123 Main St", "New York", "USA")
        user.pull_domain_events()  # Limpiar eventos
        return user, address
    
    def test_remove_address_successfully(self, handler, mock_write_repository, mock_event_dispatcher, sample_user_with_address):
        """Debería eliminar dirección exitosamente."""
        user, address = sample_user_with_address
        mock_write_repository.find_by_id.return_value = user
        mock_write_repository.save.return_value = user
        
        command = RemoveUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id=address.id.value
        )
        
        result = handler.handle(command)
        
        assert result is True
        mock_write_repository.save.assert_called_once()
        mock_event_dispatcher.publish_multiple.assert_called_once()
    
    def test_remove_address_user_not_found(self, handler, mock_write_repository):
        """Debería lanzar error si el usuario no existe."""
        mock_write_repository.find_by_id.return_value = None
        
        command = RemoveUserAddressCommand(
            user_id="nonexistent-id-00000000000000000",
            address_id="660e8400-e29b-41d4-a716-446655440001"
        )
        
        with pytest.raises(ValueError) as exc_info:
            handler.handle(command)
        
        assert "User" in str(exc_info.value)
        assert "not found" in str(exc_info.value)
    
    def test_remove_address_address_not_found(self, handler, mock_write_repository):
        """Debería lanzar error si la dirección no existe."""
        user = User.create(
            id=UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000"),
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
        mock_write_repository.find_by_id.return_value = user
        
        command = RemoveUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001"
        )
        
        with pytest.raises(ValueError) as exc_info:
            handler.handle(command)
        
        assert "Address" in str(exc_info.value)
        assert "not found" in str(exc_info.value)
