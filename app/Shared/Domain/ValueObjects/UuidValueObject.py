from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
import uuid


class UuidValueObject(StringValueObject):
    
    def __init__(self, value):
        
        if len(value) != 36:
            raise ValueError("Invalid UUID lenght")
        
        super().__init__(value)
    
    @staticmethod
    def create(value: str = None):
        
        if value is None:
            value = str(uuid.uuid4())
        
        return UuidValueObject(value)