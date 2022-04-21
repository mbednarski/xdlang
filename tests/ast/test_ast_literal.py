import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


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
def test_int(text, type, value):
    ast = parse_and_transform_expr(text)
    assert isinstance(ast, xd_ast.LiteralNode)
    assert ast.type == type
    assert ast.value == value
