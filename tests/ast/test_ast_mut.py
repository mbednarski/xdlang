import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="statement")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


# fmt: off
@pytest.mark.parametrize(
    "text,type,identifier",
    [
        ("mut x = 5;", XDType.INT, 'x'),
        ("mut y = 5.0;", XDType.FLOAT, 'y'),
        ("mut c = '*';", XDType.CHAR, 'c'),
        ("mut b = false;", XDType.BOOL, 'b'),
    ]
)
# fmt: on
def test_let(text: str, type: XDType, identifier: str):
    ast = parse_and_transform_stmt(text)
    assert isinstance(ast, xd_ast.MutStmtNode)
    assert isinstance(ast.expr, xd_ast.ExprNode)
    assert ast.identifier == identifier
