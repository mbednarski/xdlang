import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.type_check import TypeChecker
from xdlang.xdtypes import XDType


def parse_and_transform_expr(program_text: str):
    parsed = parse_text(program_text, start="expr")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


@pytest.mark.parametrize(
    "text,target_type",
    [
        ("1.7 + 2", XDType.FLOAT),
    ],
)
def test_binary_rhs(text: str, target_type: XDType):
    ast: xd_ast.BinaryNode = parse_and_transform_expr(text)
    type_checker = TypeChecker()
    type_checker.visit_expr(ast)

    assert ast.type == target_type
    assert isinstance(ast.rhs, xd_ast.CastNode)
    assert ast.rhs.type == target_type


@pytest.mark.parametrize(
    "text,target_type",
    [
        ("3 + 2.2", XDType.FLOAT),
    ],
)
def test_binary_lhs(text: str, target_type: XDType):
    ast: xd_ast.BinaryNode = parse_and_transform_expr(text)
    type_checker = TypeChecker()
    type_checker.visit_expr(ast)

    assert ast.type == target_type
    assert isinstance(ast.lhs, xd_ast.CastNode)
    assert ast.lhs.type == target_type
