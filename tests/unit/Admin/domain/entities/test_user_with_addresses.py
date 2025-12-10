"""
Tests para la gestión de direcciones en el agregado User.
"""
import pytest
from Admin.Domain.User import User
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.Events.UserAddressAdded import UserAddressAdded
from Admin.Domain.Events.UserAddressRemoved import UserAddressRemoved
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class TestUserAddresses:
    """Tests para la gestión de direcciones en User."""
    
    @pytest.fixture
    def user(self):
        """Fixture que crea un usuario para testing."""
        return User.create(
            username=UsernameValueObject.create("john_doe"),
            email=EmailValueObject.create("john@example.com")
        )
    
    def test_user_starts_with_no_addresses(self, user):
        """Verifica que un usuario nuevo no tiene direcciones."""
        assert len(user.addresses) == 0
    
    def test_add_address(self, user):
        """Verifica que se puede añadir una dirección."""
        address = user.add_address(
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        assert len(user.addresses) == 1
        assert address.street == "Calle Mayor 1"
        assert address.city == "Madrid"
        assert address.country == "España"
    
    def test_add_address_records_event(self, user):
        """Verifica que añadir dirección registra evento."""
        user.add_address(
            street="Calle Mayor 1",
            city="Madrid",
            country="España"
        )
        
        events = user.pull_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserAddressAdded)
        assert events[0].city == "Madrid"
        assert events[0].user_id == user.id.value
    
    def test_add_multiple_addresses(self, user):
        """Verifica que se pueden añadir múltiples direcciones."""
        user.add_address("Calle 1", "Madrid", "España")
        user.add_address("Calle 2", "Barcelona", "España")
        user.add_address("Calle 3", "Lisboa", "Portugal")
        
        assert len(user.addresses) == 3
    
    def test_get_address_by_id(self, user):
        """Verifica obtener dirección por ID."""
        added = user.add_address("Calle Mayor 1", "Madrid", "España")
        
        found = user.get_address(added.id)
        
        assert found is not None
        assert found.id.value == added.id.value
    
    def test_get_address_not_found(self, user):
        """Verifica que retorna None si no existe."""
        non_existent_id = UuidValueObject.create("00000000-0000-0000-0000-000000000000")
        
        found = user.get_address(non_existent_id)
        
        assert found is None
    
    def test_remove_address(self, user):
        """Verifica que se puede eliminar una dirección."""
        added = user.add_address("Calle Mayor 1", "Madrid", "España")
        user.pull_domain_events()  # Limpiar eventos previos
        
        result = user.remove_address(added.id)
        
        assert result is True
        assert len(user.addresses) == 0
    
    def test_remove_address_records_event(self, user):
        """Verifica que eliminar dirección registra evento."""
        added = user.add_address("Calle Mayor 1", "Madrid", "España")
        user.pull_domain_events()  # Limpiar eventos previos
        
        user.remove_address(added.id)
        
        events = user.pull_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserAddressRemoved)
        assert events[0].address_id == added.id.value
    
    def test_remove_non_existent_address(self, user):
        """Verifica que no se puede eliminar dirección inexistente."""
        non_existent_id = UuidValueObject.create("00000000-0000-0000-0000-000000000000")
        
        result = user.remove_address(non_existent_id)
        
        assert result is False
    
    def test_addresses_returns_copy(self, user):
        """Verifica que addresses retorna una copia (inmutabilidad)."""
        user.add_address("Calle Mayor 1", "Madrid", "España")
        
        addresses1 = user.addresses
        addresses2 = user.addresses
        
        assert addresses1 is not addresses2
        assert addresses1[0].id.value == addresses2[0].id.value
