import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_expr(program_text: str):
    parsed = parse_text(program_text, start="expr")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


# fmt: off
@pytest.mark.parametrize(
    "text,target_type",
    [
        ("cast<int> 17.4", XDType.INT),
        ("cast<float> -3", XDType.FLOAT),
        ("cast<char> 68", XDType.CHAR),
        ("cast<bool> (17.4 - 3)", XDType.BOOL),
    ],
)
# fmt: on
def test_cast(text, target_type):
    parsed: xd_ast.CastNode = parse_and_transform_expr(text)
    print(parsed)
    assert isinstance(parsed, xd_ast.CastNode)
    assert parsed.target_type == target_type
    assert isinstance(parsed.expr, xd_ast.ExprNode)


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
