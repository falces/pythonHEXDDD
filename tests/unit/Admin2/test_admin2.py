"""
Tests para Admin2.
"""
import pytest
from unittest.mock import MagicMock, patch
from Admin2.models import User
from Admin2.services import UserService


class TestUserModel:
    """Tests del modelo User."""
    
    def test_create_user(self):
        user = User(username='john', email='john@example.com')
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.id is not None
    
    def test_create_user_with_custom_id(self):
        user = User(username='john', email='john@example.com', id='custom-id')
        assert user.id == 'custom-id'
    
    def test_to_dict(self):
        user = User(username='john', email='john@example.com', id='123')
        result = user.to_dict()
        assert result == {
            'id': '123',
            'username': 'john',
            'email': 'john@example.com'
        }


class TestUserService:
    """Tests del servicio UserService."""
    
    @pytest.fixture
    def service(self):
        return UserService()
    
    @patch('Admin2.services.db')
    def test_create_user(self, mock_db, service):
        user = service.create(username='john', email='john@example.com')
        
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()
    
    @patch('Admin2.services.db')
    def test_get_by_id(self, mock_db, service):
        mock_user = MagicMock()
        mock_db.session.get.return_value = mock_user
        
        result = service.get_by_id('123')
        
        assert result == mock_user
        mock_db.session.get.assert_called_once_with(User, '123')
    
    @patch('Admin2.services.db')
    def test_get_by_id_not_found(self, mock_db, service):
        mock_db.session.get.return_value = None
        
        result = service.get_by_id('non-existent')
        
        assert result is None
    
    @patch('Admin2.services.db')
    def test_delete_success(self, mock_db, service):
        mock_user = MagicMock()
        mock_db.session.get.return_value = mock_user
        
        result = service.delete('123')
        
        assert result is True
        mock_db.session.delete.assert_called_once_with(mock_user)
        mock_db.session.commit.assert_called_once()
    
    @patch('Admin2.services.db')
    def test_delete_not_found(self, mock_db, service):
        mock_db.session.get.return_value = None
        
        result = service.delete('non-existent')
        
        assert result is False
        mock_db.session.delete.assert_not_called()
