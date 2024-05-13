from db.db import db
from constants.error_constants import ErrorConstants
import logging
from sqlalchemy.exc import IntegrityError, DataError

logger = logging.getLogger()

class Service:
    class ServiceResponse:
        def __init__(self, status_code=400, data={}) -> None:
            self.status_code = status_code
            self.data = data

    def __init__(self, model=None) -> None:
        self.model = model

    def handle_error(self, error):
        logger.warn(f"########ERRORTYPE: {type(error).__name__}") 
        logger.warn(f"ERROR: {str(error)}")
        if type(error) in (IntegrityError, DataError):
            return self.ServiceResponse(status_code=400, data=f"error: {ErrorConstants.BAD_DATA}")
        return self.ServiceResponse(status_code=500, data=f"error: {ErrorConstants.INTERNAL_SERVER_ERROR}")

    def add_data(self, instance):
        try:
            db.session.add(instance)
            db.session.commit()
            return self.ServiceResponse(status_code=200, data=instance)
        except Exception as e:  
            return self.handle_error(e)
        
    def get_data(self, id):
        try:
            instance = self.model.query.get(id)
            if not instance:
                return self.ServiceResponse(status_code=404, data=f"error: {ErrorConstants.NOT_FOUND}")
            return self.ServiceResponse(status_code=200, data=instance)
        except Exception as e: 
           return self.handle_error(e)
        
    def update_data(self, id, updated_data):
        try:
            instance = self.model.query.get(id)
            if instance:
                for key, value in updated_data.items():
                    setattr(instance, key, value)
                db.session.commit()
                return self.ServiceResponse(status_code=200, data=instance)
            else:
                return self.ServiceResponse(status_code=404, data=f"error: {ErrorConstants.NOT_FOUND}")
        except Exception as e:
            return self.handle_error(e)
        
    def delete_data(self, id):
        try:
            instance = self.model.query.get(id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
                return self.ServiceResponse(status_code=204)
            else:
                return self.ServiceResponse(status_code=404, data=f"error: {ErrorConstants.NOT_FOUND}")
        except Exception as e:
            return self.handle_error(e)
        