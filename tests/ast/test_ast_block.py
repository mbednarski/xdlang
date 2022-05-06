import pytest

from xdlang.structures import ast
from xdlang.visitors.parser import parse_text, transform_parse_tree


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="block")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


def test_block():
    text = """{
return 0;
return 1;
return 2;
}"""
    node: ast.BlockNode = parse_and_transform_stmt(text)
    assert isinstance(node, ast.BlockNode)
    assert all([isinstance(s, ast.StmtNode) for s in node.statements])
    assert len(node.statements) == 3
