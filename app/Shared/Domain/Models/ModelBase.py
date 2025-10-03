from typing import Self
class ModelBase():
    def add(
        self,
        db,
        model: Self,
    ):
        db.session.add(model)

    def getModel(self) -> Self:
        return self.model

    @staticmethod
    def commit(db):
        db.session.commit()