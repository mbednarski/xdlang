import pytest

from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xdast import BinaryOpNode, LiteralNode
from xdlang.xdtypes import XDType


def _parse_literal(program_text: str):
    tree = parse_text(program_text, start="expr")
    ast = transform_parse_tree(tree)
    return ast


@pytest.mark.parametrize(
    "program",
    [
        ("-4+3"),
        ("0-9"),
        ("3/2"),
        ("5*9"),
    ],
)
def test_arithmetic_int(program):
    tree: BinaryOpNode = _parse_literal(program)
    assert type(tree) is BinaryOpNode
    assert tree.return_type == XDType.NUMERIC


@pytest.mark.parametrize(
    "program",
    [
        ("-4>3"),
        ("0>=9"),
        ("3==2"),
        ("5<9"),
        ("5<=9"),
        ("5!=9"),
    ],
)
def test_relation_int(program):
    tree: BinaryOpNode = _parse_literal(program)
    assert type(tree) is BinaryOpNode
    assert tree.return_type == XDType.BOOL


@pytest.mark.parametrize(
    "program",
    [
        ("true and true"),
        ("false or false"),
        ("true == false"),
        ("true != false"),
    ],
)
def test_relation_bool(program):
    tree: BinaryOpNode = _parse_literal(program)
    assert type(tree) is BinaryOpNode
    assert tree.return_type == XDType.BOOL
