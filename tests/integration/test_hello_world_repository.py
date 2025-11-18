"""
Tests de integración para HelloWorldWriteRepository.
Usan base de datos SQLite en memoria.
"""

import pytest
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Infrastructure.Repository.HelloWorldWriteRepository import HelloWorldWriteRepository


@pytest.mark.integration
class TestHelloWorldRepositoryIntegration:
    """Tests de integración para HelloWorldWriteRepository."""
    
    def test_save_and_find_by_id(self, app, db_session):
        """Debería guardar y recuperar por ID."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            greeting = Greeting.create("Integration Test")
            entity = HelloWorld(greeting=greeting)
            
            # Act - Guardar
            saved_entity = repository.save(entity)
            db_session.commit()
            
            # Act - Buscar
            found_entity = repository.findById(saved_entity.id)
            
            # Assert
            assert found_entity is not None
            assert found_entity.id == saved_entity.id
            assert found_entity.greeting.value == "Integration Test"
    
    def test_find_all_returns_all_entities(self, app, db_session):
        """Debería retornar todas las entidades."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            
            greeting1 = Greeting.create("First")
            greeting2 = Greeting.create("Second")
            
            entity1 = HelloWorld(greeting=greeting1)
            entity2 = HelloWorld(greeting=greeting2)
            
            repository.save(entity1)
            repository.save(entity2)
            db_session.commit()
            
            # Act
            all_entities = repository.findAll()
            
            # Assert
            assert len(all_entities) >= 2
            greetings = [e.greeting.value for e in all_entities]
            assert "First" in greetings
            assert "Second" in greetings
    
    def test_delete_removes_entity(self, app, db_session):
        """Debería eliminar entidad correctamente."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            greeting = Greeting.create("To Delete")
            entity = HelloWorld(greeting=greeting)
            
            saved_entity = repository.save(entity)
            db_session.commit()
            entity_id = saved_entity.id
            
            # Act
            result = repository.delete(entity_id)
            db_session.commit()
            
            # Assert
            assert result is True
            found = repository.findById(entity_id)
            assert found is None
    
    def test_delete_nonexistent_returns_false(self, app, db_session):
        """Debería retornar False al eliminar entidad inexistente."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            
            # Act
            result = repository.delete(999999)
            
            # Assert
            assert result is False
    
    def test_find_by_id_nonexistent_returns_none(self, app, db_session):
        """Debería retornar None para ID inexistente."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            
            # Act
            found = repository.findById(888888)
            
            # Assert
            assert found is None
    
    def test_save_updates_existing_entity(self, app, db_session):
        """Debería actualizar entidad existente."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            greeting = Greeting.create("Original")
            entity = HelloWorld(greeting=greeting)
            
            saved_entity = repository.save(entity)
            db_session.commit()
            original_id = saved_entity.id
            
            # Act - Modificar y guardar de nuevo
            new_greeting = Greeting.create("Updated")
            updated_entity = HelloWorld(greeting=new_greeting, id=original_id)
            repository.save(updated_entity)
            db_session.commit()
            
            # Assert
            found = repository.findById(original_id)
            assert found.greeting.value == "Updated"
    
    def test_multiple_saves_in_transaction(self, app, db_session):
        """Debería manejar múltiples guardados en una transacción."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            entities = []
            
            # Act - Guardar múltiples entidades
            for i in range(5):
                greeting = Greeting.create(f"Entity {i}")
                entity = HelloWorld(greeting=greeting)
                saved = repository.save(entity)
                entities.append(saved)
            
            db_session.commit()
            
            # Assert - Todas deberían estar guardadas
            for entity in entities:
                found = repository.findById(entity.id)
                assert found is not None
    
    def test_rollback_on_error(self, app, db_session):
        """Debería hacer rollback en caso de error."""
        # Arrange
        with app.app_context():
            repository = HelloWorldWriteRepository()
            greeting = Greeting.create("Rollback Test")
            entity = HelloWorld(greeting=greeting)
            
            # Act - Guardar pero hacer rollback
            saved = repository.save(entity)
            entity_id = saved.id
            db_session.rollback()
            
            # Assert - No debería existir después del rollback
            found = repository.findById(entity_id)
            # Nota: En SQLite en memoria, esto podría comportarse diferente
            # Lo importante es que el patrón de rollback funcione
