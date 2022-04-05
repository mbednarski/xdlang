from abc import ABC, abstractmethod

import llvmlite.ir as ir

import xdlang.types as xdtypes

variables = {}


class Node(ABC):
    @abstractmethod
    def codegen(self):
        pass


class LetStmtNode(Node):
    def __init__(self, type, identifier, expr) -> None:
        self.expr = expr
        self.identifier = identifier

    def codegen(self, builder: ir.IRBuilder):
        expr_val = self.expr.codegen(builder)

        var = builder.alloca(xdtypes.int64_t, 1, name=self.identifier)
        variables[self.identifier] = var
        builder.store(expr_val, variables[self.identifier])


class IntLiteralNode(Node):
    def __init__(self, value: int):
        if type(value) != int:
            raise TypeError("value must be an int")
        self.value = value

    def codegen(self, builder: ir.builder):
        # return xdtypes.int64_t(self.value, )
        return ir.Constant(xdtypes.int64_t, self.value)

    def __repr__(self) -> str:
        return f"IntLiteralNode({self.value})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, IntLiteralNode):
            return self.value == __o.value
        return False


class LiteralNode(Node):
    def __init__(self, type_: xdtypes.IRType, value: int):
        self.value = value
        self.type_ = type_

    def codegen(self, builder: ir.builder):
        # return xdtypes.int64_t(self.value, )
        return ir.Constant(xdtypes.int64_t, self.value)

    def __repr__(self) -> str:
        return f"LiteralNode of type {self.type_} and value {self.value}"

    def __str__(self) -> str:
        return f"LiteralNode of type {self.type_} and value {self.value}"


class BinaryOpNode(Node):
    def __init__(self, lhs: Node, op: str, rhs: Node):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

        if type(lhs) != type(rhs):
            raise TypeError("lhs and rhs must be of the same type")
        if type(lhs) != LiteralNode:
            raise TypeError("lhs and rhs must be of type LiteralNode")
        
        if op in ["==", "!=", "<", "<=", ">", ">=", "or", "and"]:
            self.return_type = xdtypes.XDType.BOOL
        else:
            self.return_type = xdtypes.XDType.NUMERIC
        

    def codegen(self, builder: ir.builder):
        lval = self.lhs.codegen(builder)
        rval = self.rhs.codegen(builder)

        match self.op:
            case "+":
                retval = builder.add(lval, rval, name="added")
            case "-":
                retval = builder.sub(lval, rval, name="subtracted")
            case "*":
                retval = builder.mul(lval, rval, name="multiplied")
            case "/":
                retval = builder.div(lval, rval, name="divided")
            case _:
                assert False

        return retval

    def __repr__(self) -> str:
        return f"BinaryOpNode({self.lhs}, {self.op}, {self.rhs})"

    def __str__(self) -> str:
        return f"BinaryOpNode({self.lhs}, {self.op}, {self.rhs})"


class GetVariableNode(Node):
    def __init__(self, name: str):
        self.name = name

    def codegen(self, builder: ir.IRBuilder):
        val = builder.load(variables[self.name], name=self.name)
        return val

    def __repr__(self) -> str:
        return f"GetVariableNode({self.name})"


class ProgramNode(Node):
    def __init__(self, expressions: list):
        self.expressions = expressions

    def codegen(self, builder: ir.IRBuilder):
        for exp in self.expressions:
            exp.codegen(builder)
