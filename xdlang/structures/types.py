from enum import Enum
from pprint import pprint

from llvmlite import ir
from llvmlite.ir.types import Type as IRType
from rich import print as rprint

import abc

class TypeBase(abc.ABC):
    def __init__(self) -> None:
        pass

class PrimitiveType():
    def __init__(self, name:str) -> None:
        self.name = name
        
class XDType(Enum):
    INT = 0
    FLOAT = 1
    BOOL = 2
    CHAR = 3
    STRING = 4

    def __str__(self) -> str:
        match self:
            case XDType.INT:
                return "int"
            case XDType.FLOAT:
                return "float"
            case XDType.BOOL:
                return "bool"
            case XDType.CHAR:
                return "char"
            case XDType.STRING:
                return "string"
            case _:
                raise TypeError(f"Unknown type: {self}")

    def can_be_promoted_to(self, target: "XDType") -> bool:
        match (self, target):
            case (XDType.INT, XDType.FLOAT):
                return True
            case _:
                return False

    def get_ir_type(self) -> ir.Type:
        match self:
            case XDType.INT:
                return ir.IntType(64)
            case XDType.FLOAT:
                return ir.FloatType()
            case XDType.BOOL:
                return ir.IntType(1)
            case XDType.CHAR:
                return ir.IntType(8)
            case _:
                raise TypeError(f"Unknown type: {self}")

    @classmethod
    def from_typename(cls, typename: str):
        match typename:
            case "int":
                return XDType.INT
            case "float":
                return XDType.FLOAT
            case "bool":
                return XDType.BOOL
            case "char":
                return XDType.CHAR
            case "string":
                return XDType.STRING
            case _:
                raise TypeError(f"Invalid typename: {typename}")

    @classmethod
    def infer_from_literal(cls, literal: str):
        if literal == "true" or literal == "false":
            return cls.BOOL, literal == "true"
        if literal.startswith('"') and literal.endswith('"'):
            return cls.STRING, literal[1:-1]
        if literal.startswith("'") and literal.endswith("'"):
            if len(literal) == 3:
                return cls.CHAR, literal[1]
            else:
                raise ValueError(
                    f"Char cannot contain multiple characters! Literal >>{literal}<<"
                )
        try:
            as_numeric = float(literal)
            if "." in literal:
                return cls.FLOAT, as_numeric
            else:
                return cls.INT, int(as_numeric)
        except ValueError:
            pass
        raise ValueError(f"Cannot infer type of >>{literal}<<")


main_fn_t = ir.FunctionType(XDType.INT.get_ir_type(), ())
