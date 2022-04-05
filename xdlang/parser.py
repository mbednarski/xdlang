from pprint import pprint
from typing import Any, Tuple

from lark import Lark, ParseTree, Token, Transformer, tree
from llvmlite import ir
from rich import print as rprint

import xdlang.types as xdtypes
import xdlang.xd_ast as xdast


class XdTransformer(Transformer):
    def LITERAL(self, item):
        type_, value = xdtypes.XDType.infer_from_literal(item)
        return xdast.LiteralNode(type_, value)

    def IDENTIFIER(self, i):
        return str(i)

    def program(self, items):
        return xdast.ProgramNode(items)

    def let_stmt(self, items):
        return xdast.LetStmtNode(items[0], items[1], items[2])

    def expr(self, items):
        if len(items) == 1 and type(items[0]) is xdast.LiteralNode:
            return items[0]
        elif len(items) == 1 and type(items[0]) is str:
            return xdast.GetVariableNode(items[0])
        elif len(items) == 3:
            return xdast.BinaryOpNode(items[0], items[1], items[2])
        else:
            raise ValueError(f"Invalid expr: {items}")


def parse_text(program_text: str, start="program") -> ParseTree:
    with open("xdlang.lark", "rt") as f:
        grammar_text = f.read()

    l = Lark(grammar_text, start=start)

    parsed = l.parse(program_text)

    return parsed


def transform_parse_tree(parse_tree: ParseTree):
    transformed = XdTransformer().transform(parse_tree)
    return transformed


#  class XdTransformer(Transformer):
#     def INT_VALUE(self, items):
#         # nv = ir.NamedValue(module, xdtypes.int64_t, 'named_variable')
#         return Int64Node(int(items[0]))

#     # def binary_expr(self, items):
#     #     return BinaryExpressionNode(str(items[1]), items[0], items[2])


#     def program(self, items):
#         return ProgramNode(items)

#     def let_stmt(self, items):
#         type, name, value = items
#         type = parse_type(type)
#         return LetStmtNode(name, type, value)


#     def rvalue(self, items):
#         item = items[0]
#         if type(item) is Int64Node:
#             return item
#         elif type(item) is Token:
#             return VariableValueNode(str(item))
#         else:
#             raise Exception("Unknown rvalue type: {}".format(type(item)))


# with open('program.xd', 'rt') as f:
#     program_text = f.read()


# rprint(parsed)
# module = ir.Module('asdf')
# main_fn = ir.Function(module, xdtypes.main_fn_t, 'main')
# body = main_fn.append_basic_block('mbody')
# builder = ir.IRBuilder(body)


# variables ={}

# def parse_type(type:str)->xdtypes.IRType:
#     match type:
#         case "int64":
#             return xdtypes.int64_t
#         case _:
#             raise Exception("Unknown type: {}".format(type))

# class Int64Node:
#     def __init__(self, value) -> None:
#         self.value = value

#     def codegen(self):
#         return xdtypes.int64_t(self.value)

#     def __repr__(self) -> str:
#         return f"Int64Node({self.value})"

# class ProgramNode:
#     def __init__(self, expressions) -> None:
#         self.expressions = expressions

#     def codegen(self):
#         for exp in self.expressions:
#             exp.codegen()

# class VariableValueNode:
#     def __init__(self, name) -> None:
#         self.name = name

#     def codegen(self):
#         var = variables[self.name]
#         return builder.load(var, name=self.name)


# class LetStmtNode:
#     def __init__(self, name, type, value):
#         self.name = name
#         self.type = type
#         self.value = value

#     def codegen(self):
#         var = builder.alloca(self.type, 1, self.name)
#         variables[self.name] = var
#         val = self.value.codegen()

#         builder.store(val, var)


#     def __repr__(self) -> str:
#         return f"LetStmtNode({self.name}, {self.type}, {self.value})"

# class BinaryExpressionNode:
#     def __init__(self, op, lhs, rhs) -> None:
#         self.op = op
#         self.lhs = lhs
#         self.rhs = rhs

#     def codegen(self):
#         var_a = builder.alloca(xdtypes.int64_t, 1, 'var_a')
#         var_b = builder.alloca(xdtypes.int64_t, 1, 'var_b')

#         stored_a = builder.store(self.lhs.codegen(), ptr=var_a)
#         stored_b = builder.store(self.rhs.codegen(), ptr=var_b)

#         loaded_a = builder.load(var_a, 'loaded_a')
#         loaded_b = builder.load(var_b, 'loaded_b')

#         # lval = self.lhs.codegen()
#         # rval = self.rhs.codegen()

#         builder.add(loaded_a, loaded_b, name='added')


#     def __repr__(self) -> str:
#         return f"BinaryExpressionNode({self.op}, {self.lhs}, {self.rhs})"

# # class LetNode:
# #     def __init__(self, name, type, value) -> None:
# #         self.name = name
# #         self.type = type
# #         self.value = value

# #     def codegen(self):
# #         pass


# transformed = XdTransformer().transform(parsed)
# print(transformed)

# returned = transformed.codegen()
# print(returned)


# print(module)

# # module = ir.Module('asdf')

# # main_fn = ir.Function(module, xdtypes.main_fn_t, 'main')
# # body = main_fn.append_basic_block('mbody')
# # builder = ir.IRBuilder(body)

# # class MyTransformer(Transformer):
# #     def rvalue(self, items):
# #         # print(items)
# #         val = int(items[0])
# #         # print(val)
# #         return int64_t(val)

# #     def lvalue(self, items):
# #         # print(items)
# #         return items[0]

# #     def assign_stmt(self, items):
# #         print(items)
# #         builder.alloca()


# # MyTransformer().transform(parsed)
