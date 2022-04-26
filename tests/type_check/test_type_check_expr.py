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
    "text",
    [
        ("1.7 + 2",),
        ("1.6 + 2.1",),
    ],
)
def test_binary_expr(text):
    ast: xd_ast.ExprNode = parse_and_transform_expr(text)
    type_checker = TypeChecker()
    type_checker.visit_expr(ast)

    assert ast.type == XDType.INT
