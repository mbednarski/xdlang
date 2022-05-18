import abc

class XdType(abc.ABC):
    def __init__(self) -> None:
        self.name = None

class PrimitiveType(XdType):
    def __init__(self, name:str) -> None:
        self.name = name
        