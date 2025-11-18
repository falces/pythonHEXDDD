from typing import List, Optional
from Infrastructure.Persistence.database import db
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Persistence.SQLAlchemy.HelloWorldModel import HelloWorldModel
from Infrastructure.Persistence.Mappers.HelloWorldMapper import HelloWorldMapper


class HelloWorldRepository(HelloWorldRepositoryInterface):
    """
    Repositorio de escritura (Write Repository) para HelloWorld.
    En CQRS, este repositorio se enfoca en operaciones de escritura (CUD).
    Las operaciones de lectura están en HelloWorldReadRepository.
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

    def findById(self, id: int) -> Optional[HelloWorld]:
        """
        Busca una entidad HelloWorld por su ID.
        """
        model = db.session.query(HelloWorldModel).filter_by(id=id).first()
        
        if model is None:
            return None
            
        return HelloWorldMapper.toDomain(model)

    def findAll(self) -> List[HelloWorld]:
        """
        Obtiene todas las entidades HelloWorld.
        """
        models = db.session.query(HelloWorldModel).all()
        
        return [HelloWorldMapper.toDomain(model) for model in models]

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
