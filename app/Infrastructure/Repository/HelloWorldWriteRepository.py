from typing import Optional
from Infrastructure.Persistence.database import db
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Persistence.SQLAlchemy.HelloWorldModel import HelloWorldModel
from Infrastructure.Persistence.Mappers.HelloWorldMapper import HelloWorldMapper


class HelloWorldWriteRepository(HelloWorldRepositoryInterface):
    """
    Repositorio de escritura (Write Repository) para HelloWorld.
    En CQRS puro, este repositorio SOLO maneja operaciones de escritura (CUD).
    Para operaciones de lectura, usar HelloWorldReadRepository.
    """

    def find_by_id(self, id: int) -> Optional[HelloWorld]:
        """
        Busca una entidad HelloWorld por su ID.
        Necesario para cargar la entidad de dominio antes de modificarla.
        """
        model = db.session.query(HelloWorldModel).filter_by(id=id).first()

        if model is None:
            return None

        return HelloWorldMapper.toDomain(model)

    def save(self, hello_world: HelloWorld) -> HelloWorld:
        """
        Persiste una entidad HelloWorld en la base de datos.
        Usa merge() para manejar tanto INSERT como UPDATE.
        """
        model = HelloWorldMapper.toModel(hello_world)

        # merge() maneja automáticamente INSERT (si no existe) o UPDATE (si existe)
        merged_model = db.session.merge(model)
        db.session.commit()
        db.session.refresh(merged_model)

        # Retornar la entidad con el ID asignado
        return HelloWorldMapper.toDomain(merged_model)

    def delete(self, id: int) -> bool:
        """
        Elimina una entidad HelloWorld por su ID.
        """
        model = db.session.query(HelloWorldModel).filter_by(id=id).first()

        if model is None:
            return False

        db.session.delete(model)
        db.session.commit()

        return True
