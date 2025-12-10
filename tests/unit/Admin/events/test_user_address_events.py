"""
Tests para los eventos de UserAddress.
"""
import pytest
from Admin.Domain.Events.UserAddressAdded import UserAddressAdded
from Admin.Domain.Events.UserAddressRemoved import UserAddressRemoved


class TestUserAddressAddedEvent:
    """Tests para el evento UserAddressAdded."""
    
    def test_create_event(self):
        """Verifica la creación del evento."""
        event = UserAddressAdded(
            user_id="user-123",
            address_id="addr-456",
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        assert event.user_id == "user-123"
        assert event.address_id == "addr-456"
        assert event.street == "Calle Mayor 1"
        assert event.city == "Madrid"
        assert event.country == "España"
    
    def test_event_has_timestamp(self):
        """Verifica que el evento tiene timestamp."""
        event = UserAddressAdded(
            user_id="user-123",
            address_id="addr-456",
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        assert event.occurred_on is not None
    
    def test_event_to_dict(self):
        """Verifica la serialización del evento."""
        event = UserAddressAdded(
            user_id="user-123",
            address_id="addr-456",
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        data = event.to_dict()
        
        assert data['user_id'] == "user-123"
        assert data['address_id'] == "addr-456"
        assert data['street'] == "Calle Mayor 1"
        assert data['city'] == "Madrid"
        assert data['country'] == "España"
    
    def test_event_repr(self):
        """Verifica la representación del evento."""
        event = UserAddressAdded(
            user_id="user-123",
            address_id="addr-456",
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        repr_str = repr(event)
        
        assert "UserAddressAdded" in repr_str
        assert "user-123" in repr_str
        assert "Madrid" in repr_str


class TestUserAddressRemovedEvent:
    """Tests para el evento UserAddressRemoved."""
    
    def test_create_event(self):
        """Verifica la creación del evento."""
        event = UserAddressRemoved(
            user_id="user-123",
            address_id="addr-456"
        )
        
        assert event.user_id == "user-123"
        assert event.address_id == "addr-456"
    
    def test_event_to_dict(self):
        """Verifica la serialización del evento."""
        event = UserAddressRemoved(
            user_id="user-123",
            address_id="addr-456"
        )
        
        data = event.to_dict()
        
        assert data['user_id'] == "user-123"
        assert data['address_id'] == "addr-456"
    
    def test_event_repr(self):
        """Verifica la representación del evento."""
        event = UserAddressRemoved(
            user_id="user-123",
            address_id="addr-456"
        )
        
        repr_str = repr(event)
        
        assert "UserAddressRemoved" in repr_str
        assert "user-123" in repr_str
        assert "addr-456" in repr_str
