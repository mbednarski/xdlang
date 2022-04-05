from enum import Enum
from pprint import pprint

from lark import Lark, Transformer, tree
from llvmlite import ir
from rich import print as rprint

from llvmlite.ir.types import Type as IRType


class TypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class XDType(Enum):
    NUMERIC = 0
    BOOL = 1
    CHAR = 2
    STRING = 3

    def get_ir_type(self) -> ir.Type:
        if self == XDType.NUMERIC:
            return ir.IntType(64)
        elif self == XDType.BOOL:
            return ir.IntType(1)
        elif self == XDType.CHAR:
            return ir.IntType(8)
        elif self == XDType.STRING:
            raise TypeError(f"Type not implemented xdtype: {self}")
        else:
            raise TypeError(f"Invalid xdtype: {self}")

    @classmethod
    def infer_from_literal(cls, literal: str):
        if literal == "true" or literal == "false":
            return cls.BOOL, literal == "true"
        if literal.startswith('"') and literal.endswith('"'):
            if len(literal) == 3:
                return cls.CHAR, literal[1]
            else:
                return cls.STRING, literal[1:-1]
        try:
            as_numeric = float(literal)
            return cls.NUMERIC, as_numeric
        except ValueError:
            pass
        raise ValueError(f"Cannot infer type of >>{literal}<<")


main_fn_t = ir.FunctionType(XDType.NUMERIC.get_ir_type(), ())
