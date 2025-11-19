from Domain.HelloWorld.HelloWorld import HelloWorld


class HelloWorldSerializer:
    """
    Serializer para transformar entidades HelloWorld a formatos de salida.

    Responsable de serializar entidades de dominio a formatos
    apropiados para la capa de presentación (API, CLI, etc.).
    Pertenece a la capa de Aplicación.
    """

    @staticmethod
    def to_dict(entity: HelloWorld) -> dict:
        """
        Convierte una entidad HelloWorld a un diccionario.

        Args:
            entity: Entidad de dominio HelloWorld

        Returns:
            dict: Representación serializada de la entidad
        """
        if entity is None:
            return None

        return {
            "id": entity.id,
            "greeting": entity.greeting,
        }
