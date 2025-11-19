from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Infrastructure.Persistence.SQLAlchemy.HelloWorldModel import HelloWorldModel


class HelloWorldMapper:
    """
    Mapper para convertir entre la entidad de dominio HelloWorld 
    y el modelo de persistencia HelloWorldModel.
    """

    @staticmethod
    def toDomain(model: HelloWorldModel) -> HelloWorld:
        """
        Convierte un modelo de persistencia a una entidad de dominio.

        Args:
            model: HelloWorldModel de SQLAlchemy

        Returns:
            HelloWorld: Entidad de dominio
        """
        if model is None:
            return None

        greeting = GreetingValueObject.create(model.greeting)
        entity = HelloWorld(greeting=greeting)
        entity._id = model.id  # Asignar el ID de persistencia

        return entity

    @staticmethod
    def toModel(entity: HelloWorld) -> HelloWorldModel:
        """
        Convierte una entidad de dominio a un modelo de persistencia.

        Args:
            entity: Entidad de dominio HelloWorld

        Returns:
            HelloWorldModel: Modelo de SQLAlchemy
        """
        if entity is None:
            return None

        return HelloWorldModel(
            greeting=entity.greeting.value,
            id=getattr(entity, '_id', None)
        )
