from dataclasses import dataclass
from pprint import pprint
from typing import Any, List, Tuple

import lark
from lark import Lark, ParseTree, Token, Transformer, ast_utils, tree
from lark.lexer import Token
from llvmlite import ir
from rich import print as rprint

import xdlang.xd_ast as xd_ast
import xdlang.xdtypes as xdtypes


class XDTransformer(Transformer):
    def LITERAL(self, item: Token):
        type, value = xdtypes.XDType.infer_from_literal(item.value)
        return xd_ast.LiteralNode(item.line, item.column, type, value)

    def product(self, items: list[Token]):
        assert len(items) == 3
        return xd_ast.BinaryNode(
            items[1].line, items[1].column, items[0], items[1].value, items[2]
        )

    def sum(self, items: list[Token]):
        assert len(items) == 3
        return xd_ast.BinaryNode(
            items[1].line, items[1].column, items[0], items[1].value, items[2]
        )

    def unary_neg(self, items: list[Token]):
        return xd_ast.UnaryNegNode(items[0].line, items[0].line, items[0])

    def expr(self, items: list[Token]):
        assert len(items) == 1
        assert isinstance(items[0], xd_ast.Node)

        return items[0]

    def read_var(self, items: List[Token]):
        assert len(items) == 1
        item = items[0]
        return xd_ast.ReadVarNode(item.line, item.column, item.value)


# class XdTransformer(Transformer):


# def LITERAL(self, item):
#     return xdast.LiteralNode(type_, value)

# def IDENTIFIER(self, i):
#     return str(i)

# def block(self, items):
#     return xdast.BlockNode(items)

# def program(self, items):
#     return xdast.ProgramNode(items)

# def if_stmt(self, items):
#     return xdast.IfStmtNode(items[0], items[1], items[2])

# def let_stmt(self, items):
#     type_ = xdtypes.XDType.from_typename(items[0])
#     identifier = items[1]
#     expr = items[2]
#     return xdast.LetStmtNode(type_, identifier, expr)

# def mut_stmt(self, items):
#     identifier = items[0]
#     expr = items[1]
#     return xdast.MutStmtNode(identifier, expr)

# def print_stmt(self, items):
#     return xdast.PrintStmtNode(items[0])

# def print_nl_stmt(self, items):
#     return xdast.PrintNlNode()

# def putchar_stmt(self, items):
#     return xdast.PutcharStmtNode(items[0])

# def while_stmt(self, items):
#     return xdast.WhileStmtNode(items[0], items[1])

# def expr(self, items):
#     if len(items) == 1 and type(items[0]) is xdast.LiteralNode:
#         return items[0]
#     elif len(items) == 1 and type(items[0]) is str:
#         return xdast.GetVariableNode(items[0])
#     elif len(items) == 3:
#         return xdast.BinaryOpNode(items[0], items[1], items[2])
#     else:
#         raise ValueError(f"Invalid expr: {items}")


def parse_text(program_text: str, start="program") -> ParseTree:
    with open("grammar.lark", "rt") as f:
        grammar_text = f.read()

    l = Lark(grammar_text, start=start, ambiguity="explicit")

    parsed = l.parse(
        program_text,
    )

    return parsed


def transform_parse_tree(parse_tree: ParseTree):
    transformed = XDTransformer().transform(parse_tree)
    return transformed
