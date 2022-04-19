import pytest

from xdlang import xd_ast
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdtypes import XDType


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="statement")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


@pytest.mark.parametrize(
    "text",
    ["return 42;", "return 17.00;", "return 'Q';", "return false;", "return true;"],
)
def test_return(text):
    ast = parse_and_transform_stmt(text)
    assert isinstance(ast, xd_ast.ReturnStmtNode)
    assert isinstance(ast.expr, xd_ast.ExprNode)
