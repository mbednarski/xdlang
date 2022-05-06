import pytest

from xdlang.structures import XDType, ast
from xdlang.visitors.parser import parse_text, transform_parse_tree


def parse_and_transform_expr(program_text: str):
    parsed = parse_text(program_text, start="expr")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


@pytest.mark.parametrize(
    "text,type,value",
    [
        ("42", XDType.INT, 42),
        ("17.00", XDType.FLOAT, 17.0),
        ("'Q'", XDType.CHAR, "Q"),
        ("false", XDType.BOOL, False),
        ("true", XDType.BOOL, True),
    ],
)
def test_literal(text, type, value):
    node: ast.LiteralNode = parse_and_transform_expr(text)
    assert isinstance(node, ast.LiteralNode)
    assert node.type == type
    assert node.value == value
