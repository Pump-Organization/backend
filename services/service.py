from db.db import db
from constants.error_constants import NotFoundError


class Service:
    def __init__(self, model=None) -> None:
        self.model = model
        self.session = db.session

    def add_data(self, instance, commit=True):
        self.session.add(instance)
        if commit:
            self.session.commit()
        return instance

    def bulk_add_data(self, instances, commit=True):
        self.session.add_all(instances)
        if commit:
            self.session.commit()
        return instances

    def get_data(self, id):
        instance = self.session.get(self.model, id)
        if not instance:
            raise NotFoundError
        return instance

    def query_by_attribute(self, **attributes):
        return self.session.query(self.model).filter_by(**attributes).first()
