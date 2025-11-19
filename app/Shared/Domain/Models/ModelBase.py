from typing import Self
class ModelBase():
    def add(
        self,
        db,
        model: Self,
    ):
        db.session.add(model)

    def get_model(self) -> Self:
        return self.model

    @staticmethod
    def commit(db):
        db.session.commit()