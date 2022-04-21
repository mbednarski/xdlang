import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="block")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


def test_block():
    text = """{
NOOP;
let int x = -17;
return 0;
}"""
    ast = parse_and_transform_stmt(text)
    assert isinstance(ast, xd_ast.BlockNode)
    assert all([isinstance(s, xd_ast.StmtNode) for s in ast.statements])
