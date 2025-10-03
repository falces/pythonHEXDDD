from Shared.Domain.Repositories.AbstractRepository import AbstractRepository
from Domain.HelloWorld.HelloWorldModel import HelloWorldModel
from Domain.HelloWorld.HelloWorld import HelloWorld
from app import db


class HelloWorldRepository(AbstractRepository):
    def __init__(self):
        self.model = HelloWorldModel()

    def save(
        self,
        helloWorld: HelloWorld,
    ):
        db.session.add(helloWorld.getModel())
        db.session.commit()

    def findAll(
        self,
    ) -> list:
        return self.model.query.all()

    def findById(
        self,
        id: int,
    ) -> HelloWorld:
        return self.model.query.filter_by(id=id).first()