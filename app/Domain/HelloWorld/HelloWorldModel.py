from app import db
from sqlalchemy import Column, Integer, Sequence


class HelloWorldModel(db.Model):
    __tablename__ = 'hello_world'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    greeting = db.Column(db.String(250), unique=False, nullable=False)

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "greeting": self.greeting,
        }