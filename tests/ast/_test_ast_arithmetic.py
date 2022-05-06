import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_expr(program_text: str):
    parsed = parse_text(program_text, start="expr")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


@pytest.mark.parametrize(
    "text,op",
    [
        ("42 + 7", "+"),
        ("42 - 7", "-"),
        ("42 * 7", "*"),
        ("42 / 7", "/"),
        ("42 % 7", "%"),
        ("78.4 + 2.78", "+"),
        ("78.4 - 2.78", "-"),
        ("78.4 / 2.78", "/"),
        ("78.4 * 2.78", "*"),
    ],
)
# fmt: on
def test_simple_arithmetic(text, op):
    parsed: xd_ast.BinaryNode = parse_and_transform_expr(text)
    assert isinstance(parsed, xd_ast.BinaryNode)
    assert isinstance(parsed.lhs, xd_ast.ExprNode)
    assert isinstance(parsed.rhs, xd_ast.ExprNode)
    parsed.operator == op


def test_unary_arithmetic():
    text = "-42"
    parsed = parse_and_transform_expr(text)
    assert isinstance(parsed, xd_ast.UnaryNegNode)
    assert isinstance(parsed.expr, xd_ast.LiteralNode)
    assert parsed.expr.type == XDType.INT
    assert parsed.expr.value == 42


def test_double_minus():
    text = "--42"
    parsed = parse_and_transform_expr(text)
    assert isinstance(parsed, xd_ast.UnaryNegNode)
    assert isinstance(parsed.expr, xd_ast.UnaryNegNode)
    assert isinstance(parsed.expr.expr, xd_ast.LiteralNode)
    assert parsed.expr.expr.type == XDType.INT
    assert parsed.expr.expr.value == 42
