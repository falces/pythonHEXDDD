from Infrastructure.Persistence.database import db
from sqlalchemy import Column, Integer, String, Sequence


class HelloWorldModel(db.Model):
    """
    Modelo de persistencia SQLAlchemy para HelloWorld.
    Este modelo pertenece a la capa de Infrastructure y no debe ser usado fuera de ella.
    """
    __tablename__ = 'hello_world'

    id = Column(Integer, Sequence('hello_world_id_seq'), primary_key=True)
    greeting = Column(String(250), unique=False, nullable=False)

    def __init__(self, greeting: str, id: int = None):
        self.id = id
        self.greeting = greeting
