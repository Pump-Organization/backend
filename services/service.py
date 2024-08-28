from db.db import db
from constants.error_constants import CUSTOM_ERRORS, AppError, NotFoundError, BadDataError
from sqlalchemy.exc import IntegrityError, DataError


class Service:
    def __init__(self, model=None) -> None:
        self.model = model
        self.session = db.session

    def add_data(self, instance, commit=True):
        self.session.add(instance)
        if commit:
            self.session.commit()
        return instance
        
    def get_data(self, id):
        instance = self.model.query.get(id)
        if not instance:
            raise NotFoundError
        return instance
        
    def query_by_attribute(self, **attributes):
        return self.session.query(self.model).filter_by(**attributes).first()
        