from db.db import db
from constants.error_constants import CUSTOM_ERRORS, AppError, NotFoundError, BadDataError
from sqlalchemy.exc import IntegrityError, DataError


class Service:
    class ServiceResponse:
        def __init__(self, status_code=400, data={}) -> None:
            self.status_code = status_code
            self.data = data

    def __init__(self, model=None) -> None:
        self.model = model
        self.session = db.session

    def handle_error(self, error):
        if type(error) in CUSTOM_ERRORS:
            raise error
        if type(error) in (IntegrityError, DataError, LookupError):
            raise BadDataError(str(error))
        if type(error) == NotFoundError:
            raise NotFoundError(str(error))
        raise AppError

    def add_data(self, instance, commit=True):
        try:
            self.session.add(instance)
            if commit:
                self.session.commit()
            return self.ServiceResponse(status_code=200, data=instance)
        except Exception as e:  
            return self.handle_error(e)
        
    def get_data(self, id):
        try:
            instance = self.model.query.get(id)
            if not instance:
                raise NotFoundError
            return self.ServiceResponse(status_code=200, data=instance)
        except Exception as e: 
           return self.handle_error(e)
        
    def query_by_attribute(self, **attributes):
        try:
            return self.ServiceResponse(status_code=200, data=self.session.query(self.model).filter_by(**attributes).first())
        except Exception as e:
           return self.handle_error(e)
        