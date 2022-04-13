import pytest

from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xd_ast import BinaryOpNode, LetStmtNode, LiteralNode
from xdlang.xdtypes import XDType


def _parse_stmt(program_text: str):
    tree = parse_text(program_text, start="let_stmt")
    ast = transform_parse_tree(tree)
    return ast


@pytest.mark.parametrize(
    "program",
    ["let numeric x = 0;"],
)
def test_basic_let(program):
    tree: LetStmtNode = _parse_stmt(program)
    assert type(tree) is LetStmtNode
    assert tree.identifier == "x"
    assert tree.type_ == XDType.NUMERIC
    assert type(tree.expr) is LiteralNode
    assert tree.expr.value == 0
    assert tree.expr.type_ == XDType.NUMERIC
