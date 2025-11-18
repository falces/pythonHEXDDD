"""
Tests de integración para HelloWorldWriteRepository.
Usan base de datos SQLite en memoria.
CQRS Puro: Write Repository solo tiene save() y delete().
Para verificar, usamos ReadRepository.
"""

import pytest
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Infrastructure.Repository.HelloWorldWriteRepository import HelloWorldWriteRepository
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository


@pytest.mark.integration
class TestHelloWorldRepositoryIntegration:
    """Tests de integración para HelloWorldWriteRepository (CQRS Puro)."""
    
    def test_save_creates_entity(self, app, db_session):
        """Debería guardar entidad correctamente."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            read_repo = HelloWorldReadRepository()
            greeting = Greeting.create("Integration Test")
            entity = HelloWorld(greeting=greeting)
            
            # Act - Guardar con Write Repository
            saved_entity = write_repo.save(entity)
            db_session.commit()
            
            # Assert - Verificar con Read Repository
            found_entity = read_repo.findById(saved_entity.id)
            assert found_entity is not None
            assert found_entity.id == saved_entity.id
            assert found_entity.greeting.value == "Integration Test"
    
    def test_save_multiple_entities(self, app, db_session):
        """Debería guardar múltiples entidades."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            read_repo = HelloWorldReadRepository()
            
            greeting1 = Greeting.create("First")
            greeting2 = Greeting.create("Second")
            
            entity1 = HelloWorld(greeting=greeting1)
            entity2 = HelloWorld(greeting=greeting2)
            
            # Act - Guardar con Write Repository
            write_repo.save(entity1)
            write_repo.save(entity2)
            db_session.commit()
            
            # Assert - Verificar con Read Repository
            all_entities = read_repo.find_all()
            assert len(all_entities) >= 2
            greetings = [e.greeting.value for e in all_entities]
            assert "First" in greetings
            assert "Second" in greetings
    
    def test_delete_removes_entity(self, app, db_session):
        """Debería eliminar entidad correctamente."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            read_repo = HelloWorldReadRepository()
            greeting = Greeting.create("To Delete")
            entity = HelloWorld(greeting=greeting)
            
            saved_entity = write_repo.save(entity)
            db_session.commit()
            entity_id = saved_entity.id
            
            # Act - Eliminar con Write Repository
            result = write_repo.delete(entity_id)
            db_session.commit()
            
            # Assert - Verificar con Read Repository
            assert result is True
            found = read_repo.findById(entity_id)
            assert found is None
    
    def test_delete_nonexistent_returns_false(self, app, db_session):
        """Debería retornar False al eliminar entidad inexistente."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            
            # Act
            result = write_repo.delete(999999)
            
            # Assert
            assert result is False
    
    def test_save_updates_existing_entity(self, app, db_session):
        """Debería actualizar entidad existente."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            read_repo = HelloWorldReadRepository()
            greeting = Greeting.create("Original")
            entity = HelloWorld(greeting=greeting)
            
            saved_entity = write_repo.save(entity)
            db_session.commit()
            original_id = saved_entity.id
            
            # Act - Modificar y guardar de nuevo
            new_greeting = Greeting.create("Updated")
            updated_entity = HelloWorld(greeting=new_greeting, id=original_id)
            write_repo.save(updated_entity)
            db_session.commit()
            
            # Assert - Verificar con Read Repository
            found = read_repo.findById(original_id)
            assert found.greeting.value == "Updated"
    
    def test_multiple_saves_in_transaction(self, app, db_session):
        """Debería manejar múltiples guardados en una transacción."""
        # Arrange
        with app.app_context():
            write_repo = HelloWorldWriteRepository()
            read_repo = HelloWorldReadRepository()
            entities = []
            
            # Act - Guardar múltiples entidades
            for i in range(5):
                greeting = Greeting.create(f"Entity {i}")
                entity = HelloWorld(greeting=greeting)
                saved = write_repo.save(entity)
                entities.append(saved)
            
            db_session.commit()
            
            # Assert - Verificar con Read Repository
            for entity in entities:
                found = read_repo.findById(entity.id)
                assert found is not None
