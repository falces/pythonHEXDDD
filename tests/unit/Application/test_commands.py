"""
Tests unitarios para Commands (CQRS).
Valida que los comandos sean inmutables y validen correctamente.
"""

import pytest
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.UpdateHelloWorldCommand import UpdateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand


class TestCreateHelloWorldCommand:
    """Tests para CreateHelloWorldCommand"""
    
    def test_create_command_with_valid_data(self):
        """Debe crear comando con datos válidos"""
        command = CreateHelloWorldCommand(greeting_text="Hello World")
        
        assert command.greeting_text == "Hello World"
    
    def test_create_command_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        command = CreateHelloWorldCommand(greeting_text="Hello World")
        
        with pytest.raises(AttributeError):
            command.greeting_text = "New greeting"
    
    def test_create_command_validates_string_type(self):
        """Debe rechazar tipo no string"""
        with pytest.raises(TypeError, match="greeting_text must be a string"):
            CreateHelloWorldCommand(greeting_text=123)


class TestUpdateHelloWorldCommand:
    """Tests para UpdateHelloWorldCommand"""
    
    def test_update_command_with_valid_data(self):
        """Debe crear comando con datos válidos"""
        command = UpdateHelloWorldCommand(id=1, greeting_text="Updated greeting")
        
        assert command.id == 1
        assert command.greeting_text == "Updated greeting"
    
    def test_update_command_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        command = UpdateHelloWorldCommand(id=1, greeting_text="Test")
        
        with pytest.raises(AttributeError):
            command.id = 2
        
        with pytest.raises(AttributeError):
            command.greeting_text = "New greeting"
    
    def test_update_command_validates_positive_id(self):
        """Debe rechazar ID no positivo"""
        with pytest.raises(ValueError, match="id must be a positive integer"):
            UpdateHelloWorldCommand(id=0, greeting_text="Test")
        
        with pytest.raises(ValueError, match="id must be a positive integer"):
            UpdateHelloWorldCommand(id=-1, greeting_text="Test")
    
    def test_update_command_validates_string_type(self):
        """Debe rechazar tipo no string"""
        with pytest.raises(TypeError, match="greeting_text must be a string"):
            UpdateHelloWorldCommand(id=1, greeting_text=123)


class TestDeleteHelloWorldCommand:
    """Tests para DeleteHelloWorldCommand"""
    
    def test_delete_command_with_valid_data(self):
        """Debe crear comando con datos válidos"""
        command = DeleteHelloWorldCommand(id=1)
        
        assert command.id == 1
    
    def test_delete_command_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        command = DeleteHelloWorldCommand(id=1)
        
        with pytest.raises(AttributeError):
            command.id = 2
    
    def test_delete_command_validates_positive_id(self):
        """Debe rechazar ID no positivo"""
        with pytest.raises(ValueError, match="id must be a positive integer"):
            DeleteHelloWorldCommand(id=0)
        
        with pytest.raises(ValueError, match="id must be a positive integer"):
            DeleteHelloWorldCommand(id=-1)
