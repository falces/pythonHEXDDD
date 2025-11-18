"""
Repositorio de lectura optimizado para HelloWorld.
Separado del repositorio de escritura según CQRS.
"""

from typing import List, Optional
from sqlalchemy import select, func
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Infrastructure.Persistence.SQLAlchemy.HelloWorldModel import HelloWorldModel
from Infrastructure.Persistence.database import db


class HelloWorldReadRepository:
    """
    Repositorio optimizado para operaciones de lectura.
    Usa queries SQL directas y puede incluir joins, índices específicos, etc.
    No tiene lógica de dominio, solo recuperación de datos.
    """
    
    def find_by_id(self, id: int) -> Optional[HelloWorldReadModel]:
        """
        Busca un HelloWorld por ID.
        Query optimizada para lectura.
        
        Args:
            id: ID del HelloWorld
            
        Returns:
            HelloWorldReadModel o None
        """
        stmt = select(HelloWorldModel).where(HelloWorldModel.id == id)
        model = db.session.execute(stmt).scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_read_model(model)
    
    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> List[HelloWorldReadModel]:
        """
        Obtiene todos los HelloWorld con paginación y ordenamiento.
        
        Args:
            limit: Número máximo de resultados
            offset: Desplazamiento
            sort_by: Campo para ordenar
            sort_order: 'asc' o 'desc'
            
        Returns:
            Lista de HelloWorldReadModel
        """
        stmt = select(HelloWorldModel)
        
        # Ordenamiento
        if sort_order == 'desc':
            stmt = stmt.order_by(getattr(HelloWorldModel, sort_by).desc())
        else:
            stmt = stmt.order_by(getattr(HelloWorldModel, sort_by).asc())
        
        # Paginación
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        
        models = db.session.execute(stmt).scalars().all()
        
        return [self._to_read_model(model) for model in models]
    
    def search(
        self,
        search_text: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[HelloWorldReadModel]:
        """
        Busca HelloWorld con criterios específicos.
        
        Args:
            search_text: Texto a buscar en el greeting
            limit: Número máximo de resultados
            offset: Desplazamiento
            
        Returns:
            Lista de HelloWorldReadModel
        """
        stmt = select(HelloWorldModel)
        
        # Filtro de búsqueda
        if search_text:
            search_pattern = f"%{search_text}%"
            stmt = stmt.where(HelloWorldModel.greeting.like(search_pattern))
        
        # Paginación
        stmt = stmt.offset(offset).limit(limit)
        
        models = db.session.execute(stmt).scalars().all()
        
        return [self._to_read_model(model) for model in models]
    
    def count(self) -> int:
        """
        Cuenta el total de HelloWorld.
        
        Returns:
            int: Total de registros
        """
        stmt = select(func.count(HelloWorldModel.id))
        return db.session.execute(stmt).scalar_one()
    
    def count_by_search(self, search_text: Optional[str] = None) -> int:
        """
        Cuenta HelloWorld que coinciden con el criterio de búsqueda.
        
        Args:
            search_text: Texto a buscar
            
        Returns:
            int: Total de registros que coinciden
        """
        stmt = select(func.count(HelloWorldModel.id))
        
        if search_text:
            search_pattern = f"%{search_text}%"
            stmt = stmt.where(HelloWorldModel.greeting.like(search_pattern))
        
        return db.session.execute(stmt).scalar_one()
    
    def _to_read_model(self, model: HelloWorldModel) -> HelloWorldReadModel:
        """
        Convierte un modelo SQLAlchemy a ReadModel.
        
        Args:
            model: Modelo de SQLAlchemy
            
        Returns:
            HelloWorldReadModel
        """
        return HelloWorldReadModel(
            id=model.id,
            greeting=model.greeting,
            created_at=None,  # Agregar si existe en el modelo
            updated_at=None   # Agregar si existe en el modelo
        )
