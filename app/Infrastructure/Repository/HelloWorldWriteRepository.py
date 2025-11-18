from typing import List, Optional
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

    def save(self, hello_world: HelloWorld) -> HelloWorld:
        """
        Persiste una entidad HelloWorld en la base de datos.
        """
        model = HelloWorldMapper.toModel(hello_world)
        
        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)
        
        # Retornar la entidad con el ID asignado
        return HelloWorldMapper.toDomain(model)

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
