"""
Tests unitarios para los Commands de UserAddress.
"""

import pytest
from Admin.Application.Commands.AddUserAddressCommand import AddUserAddressCommand
from Admin.Application.Commands.UpdateUserAddressCommand import UpdateUserAddressCommand
from Admin.Application.Commands.RemoveUserAddressCommand import RemoveUserAddressCommand


class TestAddUserAddressCommand:
    """Tests para AddUserAddressCommand."""
    
    def test_create_command(self):
        """Debería crear comando con datos válidos."""
        command = AddUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        
        assert command.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert command.street == "123 Main St"
        assert command.city == "New York"
        assert command.country == "USA"
    
    def test_command_is_immutable(self):
        """El comando debería ser inmutable (frozen=True)."""
        command = AddUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            street="123 Main St",
            city="New York",
            country="USA"
        )
        
        with pytest.raises(Exception):
            command.street = "456 Other St"


class TestUpdateUserAddressCommand:
    """Tests para UpdateUserAddressCommand."""
    
    def test_create_command_with_all_fields(self):
        """Debería crear comando con todos los campos."""
        command = UpdateUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001",
            street="456 Updated St",
            city="Los Angeles",
            country="USA"
        )
        
        assert command.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert command.address_id == "660e8400-e29b-41d4-a716-446655440001"
        assert command.street == "456 Updated St"
        assert command.city == "Los Angeles"
        assert command.country == "USA"
    
    def test_create_command_with_partial_fields(self):
        """Debería crear comando con campos parciales."""
        command = UpdateUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001",
            street="456 Updated St"
        )
        
        assert command.street == "456 Updated St"
        assert command.city is None
        assert command.country is None
    
    def test_command_is_immutable(self):
        """El comando debería ser inmutable (frozen=True)."""
        command = UpdateUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001",
        )
        
        with pytest.raises(Exception):
            command.street = "New Street"


class TestRemoveUserAddressCommand:
    """Tests para RemoveUserAddressCommand."""
    
    def test_create_command(self):
        """Debería crear comando con datos válidos."""
        command = RemoveUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001"
        )
        
        assert command.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert command.address_id == "660e8400-e29b-41d4-a716-446655440001"
    
    def test_command_is_immutable(self):
        """El comando debería ser inmutable (frozen=True)."""
        command = RemoveUserAddressCommand(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            address_id="660e8400-e29b-41d4-a716-446655440001"
        )
        
        with pytest.raises(Exception):
            command.address_id = "new-id"
