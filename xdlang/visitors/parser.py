from dataclasses import dataclass
from pprint import pprint
from typing import Any, List, Tuple

import lark
from lark import Lark, ParseTree, Token, Transformer, ast_utils, tree
from lark.lexer import Token
from llvmlite import ir
from rich import print as rprint

from xdlang.structures import XDType
from xdlang.structures import ast as ast


class XDTransformer(Transformer):
    def LITERAL(self, item: Token):
        type, value = XDType.infer_from_literal(item.value)
        return ast.LiteralNode(item.line, item.column, type, value)

    def prod_expr(self, items: list[ast.Node | Token]):
        assert len(items) == 3
        assert isinstance(items[0], ast.Node)
        assert isinstance(items[1], Token)
        assert isinstance(items[2], ast.Node)
        return ast.BinaryNode(
            items[1].line, items[1].column, items[0], items[1].value, items[2]
        )

    def sum_expr(self, items: list[ast.Node | Token]):
        assert len(items) == 3
        assert isinstance(items[0], ast.Node)
        assert isinstance(items[1], Token)
        assert isinstance(items[2], ast.Node)
        return ast.BinaryNode(
            items[1].line, items[1].column, items[0], items[1].value, items[2]
        )

    def unary_minus(self, items: list[ast.Node]):
        return ast.UnaryNegNode(items[0].line, items[0].line, items[0])

    def expr(self, items: list[Token]):
        assert len(items) == 1
        assert isinstance(items[0], ast.Node)

        return items[0]

    def cast_expr(self, items):
        assert len(items) == 2

        target_type = XDType.from_typename(items[0])
        return ast.CastNode(items[0].line, items[0].column, target_type, items[1])

    def read_var(self, items: List[Token]):
        assert len(items) == 1
        item = items[0]
        return ast.ReadVarNode(item.line, item.column, item.value)

    def let_stmt(self, items: List[Token | ast.Node]):
        assert len(items) == 3
        assert isinstance(items[0], Token)
        assert isinstance(items[1], Token)
        assert isinstance(items[2], ast.Node)

        return ast.LetStmtNode(
            items[0].line,
            items[0].column,
            XDType.from_typename(items[0].value),
            items[1].value,
            items[2],
        )

    def noop_stmt(self, items):
        return ast.NoopStmtNode(items[0].line, items[0].column)

    def return_stmt(self, items):
        assert isinstance(items[1], ast.Node)
        return ast.ReturnStmtNode(items[0].line, items[0].column, items[1])

    def block(slf, items):
        # TODO: empty stmt
        statements = items[1:-1]
        return ast.BlockNode(items[0].line, items[0].column, statements)

    def program(self, items):
        return ast.ProgramNode(0, 0, items[0])

    def mut_stmt(self, items):
        return ast.MutStmtNode(items[0].line, items[0].column, items[0], items[1])

    def func_stmt(self, items: List[Token]):
        identifier = items[0].value
        typename = items[-2].value
        args = []
        body = items[-1]

        type = XDType.from_typename(typename)

        return ast.FuncDefinitionNode(
            items[0].line, items[1].column, identifier, args, type, body
        )

    def __default__(self, data, children, meta):
        assert False


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
