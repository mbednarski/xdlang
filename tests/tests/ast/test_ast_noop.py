import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="statement")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


def test_noop_stmt():
    ast = parse_and_transform_stmt("NOOP;")
    assert isinstance(ast, xd_ast.NoopStmtNode)
