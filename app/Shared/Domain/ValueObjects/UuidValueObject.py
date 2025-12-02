from Shared.Domain.ValueObjects.StringValueObject import StringValueObject


class UuidValueObject(StringValueObject):
    
    def __init__(self, value):
        super().__init__(value)
        
        if len(value) != 36:
            raise ValueError("Invalid UUID lenght")
    
    @staticmethod
    def create(value):
        return UuidValueObject(value)