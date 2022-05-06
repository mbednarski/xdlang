import pytest

from xdlang.structures import XDType, ast
from xdlang.visitors.parser import parse_text, transform_parse_tree


def parse_and_transform_stmt(program_text: str):
    parsed = parse_text(program_text, start="statement")
    ast = transform_parse_tree(parse_tree=parsed)
    return ast


@pytest.mark.parametrize(
    "text",
    ["return 42;", "return 17.00;", "return 'Q';", "return false;", "return true;"],
)
def test_return(text):
    node: ast.ReturnStmtNode = parse_and_transform_stmt(text)
    assert isinstance(node, ast.ReturnStmtNode)
    assert isinstance(node.expr, ast.ExprNode)
