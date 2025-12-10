"""
Tests unitarios para la entidad UserAddress.
"""
import pytest
from Admin.Domain.Entities.UserAddress import UserAddress
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class TestUserAddress:
    """Tests para la entidad UserAddress."""
    
    def test_create_address(self):
        """Verifica la creación de una dirección."""
        address = UserAddress.create(
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        assert address.street == "Calle Mayor 1"
        assert address.city == "Madrid"
        assert address.country == "España"
        assert address.id is not None
    
    def test_create_address_with_custom_id(self):
        """Verifica la creación con ID personalizado."""
        custom_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000")
        address = UserAddress.create(
            street="Calle Mayor 1",
            city="Madrid",
            country="España",
            id=custom_id
        )
        
        assert address.id.value == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_update_address(self):
        """Verifica la actualización de una dirección."""
        address = UserAddress.create(
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        address.update(street="Calle Nueva 2", city="Barcelona")
        
        assert address.street == "Calle Nueva 2"
        assert address.city == "Barcelona"
        assert address.country == "España"  # No cambió
    
    def test_update_address_partial(self):
        """Verifica actualización parcial."""
        address = UserAddress.create(
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        address.update(country="Portugal")
        
        assert address.street == "Calle Mayor 1"
        assert address.city == "Madrid"
        assert address.country == "Portugal"
