from abc import ABC, abstractmethod
from typing import Any

import llvmlite.ir as ir

from xdlang.xdtypes import XDType


class Node:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def accept(self, visitor):
        pass


class LiteralNode(Node):
    def __init__(self, line: int, column: int, type: XDType, value: Any):
        super().__init__(line, column)
        self.value = value
        self.type = type

    def accept(self, visitor) -> Any:
        return visitor.visit_literal(self)

    # def __str__(self) -> str:
    #     return f"{self.line}:{self.column} LiteralNode of type {self.type} and value {self.value}"


class BinaryNode(Node):
    def __init__(self, line: int, column: int, lhs: Node, operator: str, rhs: Node):
        super().__init__(line, column)
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def accept(self, visitor):
        return visitor.visit_binary(self)


class UnaryNegNode(Node):
    def __init__(self, line: int, column: int, operand: Node):
        super().__init__(line, column)
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_neg(self)


class ReadVarNode(Node):
    def __init__(self, line: int, column: int, identifier: str):
        super().__init__(line, column)
        self.identifier = identifier

    def accept(self, visitor):
        return visitor.visit_read_var(self)

    # def __str__(self):
    #     return f"{self.line}:{self.column} BinaryNode:{self.operator}"

    # def __repr__(self):
    #     return f"{self.line}:{self.column} BinaryNode:{self.operator}"


# class Node(ABC):
#     def codegen(self):
#         pass


# class PutcharStmtNode(Node):
#     def __init__(self, expr) -> None:
#         self.arg = expr

#     def codegen(self, builder: ir.IRBuilder):
#         v = self.arg.codegen(builder)
#         extended = builder.zext(
#             v,
#             ir.IntType(32),
#         )
#         builder.call(builder.module.get_global("putchar"), [extended])
#         pass


# class PrintNlNode(Node):
#     def codegen(self, builder: ir.IRBuilder):
#         int32 = ir.IntType(32)
#         builder.call(builder.module.get_global("putchar"), [int32(ord("\n"))])


# class MutStmtNode(Node):
#     def __init__(self, identifier, expr) -> None:
#         self.identifier = identifier
#         self.expr = expr

#     def accept(self, visitor):
#         expr_val = self.expr.accept(visitor)
#         visitor.visit_mut_stmt(self, expr_val)

#     # def codegen(self, builder:ir.IRBuilder):
#     #     if not variables.exists(self.identifier):
#     #         raise TypeError(f"Variable {self.identifier} does not exist")

#     #     var = variables.get(self.identifier)
#     #     if var.type_ != self.expr.type_:
#     #         raise TypeError("Variable {} is of type {}, but expression is of type {}".format(
#     #             self.identifier, var.type_, self.expr.type_))

#     #     val = self.expr.codegen(builder)
#     #     builder.store(val, var.var)


# class PrintStmtNode(Node):
#     def __init__(self, text: str):
#         self.text = text

#     def codegen(self, builder: ir.IRBuilder):
#         array_type = ir.ArrayType(ir.IntType(8), len(self.text) + 1)
#         c = ir.GlobalVariable(builder.module, array_type, "str1")
#         c.global_constant = True
#         c.initializer = array_type([ord(c) for c in self.text + "\0"])

#         t = ir.IntType(32)
#         elemptr = builder.gep(c, (t(0),), name="elemptr")

#         puts = builder.module.get_global("puts")
#         call = builder.call(puts, (elemptr,))
#         return call


# class LetStmtNode(Node):
#     def __init__(self, type_: xdtypes.XDType, identifier: str, expr) -> None:
#         self.expr = expr
#         self.identifier = identifier
#         self.type_ = type_

#     def accept(self, visitor):
#         expr_val = self.expr.accept(visitor)
#         visitor.visit_let_stmt(self, expr_val)

#     def codegen(self, builder: ir.IRBuilder):

#         expr_val = self.expr.codegen(builder)

#         if self.type_ == xdtypes.XDType.STRING:
#             t = ir.IntType(32)
#             elemptr = builder.gep(expr_val, (t(0),), name="elemptr")

#         var = builder.alloca(self.type_.get_ir_type(), 1, name=self.identifier)
#         variables.add_variable(
#             Variable(identifier=self.identifier, type_=self.type_, var=var)
#         )
#         stored = builder.store(expr_val, var)
#         return stored


# class IntLiteralNode(Node):
#     def __init__(self, value: int):
#         if type(value) != int:
#             raise TypeError("value must be an int")
#         self.value = value

#     def codegen(self, builder: ir.builder):
#         # return xdtypes.int64_t(self.value, )
#         return ir.Constant(xdtypes.int64_t, self.value)

#     def __repr__(self) -> str:
#         return f"IntLiteralNode({self.value})"

#     def __eq__(self, __o: object) -> bool:
#         if isinstance(__o, IntLiteralNode):
#             return self.value == __o.value
#         return False


# class LiteralNode(Node):
#     def __init__(self, type_: xdtypes.IRType, value):
#         self.value = value
#         self.type_ = type_

#     def accept(self, visitor):
#         return visitor.visit_literal(self)

#     def codegen(self, builder: ir.builder):
#         # return xdtypes.int64_t(self.value, )
#         if self.type_ == xdtypes.XDType.STRING:
#             array_type = ir.ArrayType(ir.IntType(8), len(self.value) + 1)
#             c = ir.GlobalVariable(builder.module, array_type, "str1")
#             c.global_constant = True
#             return c

#         if self.type_ == xdtypes.XDType.CHAR:
#             return ir.Constant(self.type_.get_ir_type(), ord(self.value))

#         return ir.Constant(self.type_.get_ir_type(), self.value)

#     def __repr__(self) -> str:
#         return f"LiteralNode of type {self.type_} and value {self.value}"

#     def __str__(self) -> str:
#         return f"LiteralNode of type {self.type_} and value {self.value}"


# class BinaryOpNode(Node):
#     def __init__(self, lhs: Node, op: str, rhs: Node):
#         self.lhs = lhs
#         self.op = op
#         self.rhs = rhs

#         if type(lhs) != type(rhs):
#             raise TypeError("lhs and rhs must be of the same type")
#         if type(lhs) != LiteralNode:
#             raise TypeError("lhs and rhs must be of type LiteralNode")

#         if op in ["==", "!=", "<", "<=", ">", ">=", "or", "and"]:
#             self.type_ = xdtypes.XDType.BOOL
#         else:
#             self.type_ = lhs.type_

#     def accept(self, visitor):
#         lval = self.lhs.accept(visitor)
#         rval = self.rhs.accept(visitor)

#         return visitor.visit_binary_op(self, lval, rval)

#     def codegen(self, builder: ir.builder):
#         lval = self.lhs.codegen(builder)
#         rval = self.rhs.codegen(builder)

#         match self.op:
#             case "+":
#                 retval = builder.add(lval, rval, name="added")
#             case "-":
#                 retval = builder.sub(lval, rval, name="subtracted")
#             case "*":
#                 retval = builder.mul(lval, rval, name="multiplied")
#             case "/":
#                 retval = builder.div(lval, rval, name="divided")
#             case _:
#                 assert False

#         return retval

#     def __repr__(self) -> str:
#         return f"BinaryOpNode({self.lhs}, {self.op}, {self.rhs})"

#     def __str__(self) -> str:
#         return f"BinaryOpNode({self.lhs}, {self.op}, {self.rhs})"


# class GetVariableNode(Node):
#     def __init__(self, identifier: str):
#         self.identifier = identifier

#     def accept(self, visitor):
#         return visitor.visit_get_variable(self)

#     def codegen(self, builder: ir.builder):
#         pass

#     def __repr__(self) -> str:
#         return f"GetVariableNode({self.identifier})"

#     def __str__(self) -> str:
#         return f"GetVariableNode({self.identifier})"


# class BlockNode(Node):
#     def __init__(self, statements: list) -> None:
#         self.statements = statements

#     def codegen(self, builder: ir.IRBuilder):
#         for stmt in self.statements:
#             stmt.codegen(builder)

#     def accept(self, visitor):
#         visitor.visit_block(self)
#         for stmt in self.statements:
#             stmt.accept(visitor)


# class IfStmtNode(Node):
#     def __init__(self, condition, if_block, else_block=None) -> None:
#         self.condition = condition  # expr i1
#         self.if_block = if_block
#         self.else_block = else_block

#     def accept(self, visitor):
#         condition_code = self.condition.accept(visitor)
#         if_code = self.if_block.accept(visitor)
#         else_code = self.else_block.accept(visitor)
#         visitor.visit_if_stmt(self, condition_code, if_code, else_code)

#     def codegen(self, builder: ir.IRBuilder):
#         pass


# class WhileStmtNode(Node):
#     def __init__(self, condition, body):
#         self.condition = condition
#         self.body = body

#     def accept(self, visitor):
#         visitor.visit_while_stmt(self)


# class ProgramNode(Node):
#     def __init__(self, items: list):
#         self.block = items[0]

#     def codegen(self, builder: ir.IRBuilder):
#         self.block.codegen(builder)

#     def accept(self, visitor):
#         visitor.visit_program(self)
#         self.block.accept(visitor)
