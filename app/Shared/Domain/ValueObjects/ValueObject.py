class ValueObject:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, ValueObject):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return str(self.value)