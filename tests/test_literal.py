import pytest

from xdlang.types import XDType
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xd_ast import LiteralNode


def _parse_literal(program_text: str):
    tree = parse_text(program_text, start="expr")
    ast = transform_parse_tree(tree)
    return ast


@pytest.mark.parametrize(
    "program,value",
    [
        ("0", 0),
        ("42", 42.0),
        ("-99", -99.0),
        ("0.1", 0.1),
        ("-0.1", -0.1),
    ],
)
def test_int_literal(program, value):
    tree: LiteralNode = _parse_literal(program)
    assert type(tree) is LiteralNode
    assert tree.type_ == XDType.NUMERIC
    assert tree.value == value


@pytest.mark.parametrize(
    "program,value",
    [
        ("true", True),
        ("false", False),
    ],
)
def test_bool_literal(program, value):
    tree: LiteralNode = _parse_literal(program)
    assert type(tree) is LiteralNode
    assert tree.type_ == XDType.BOOL
    assert tree.value == value


@pytest.mark.parametrize(
    "program,value",
    [
        ("true", True),
        ("false", False),
    ],
)
def test_bool_literal(program, value):
    tree: LiteralNode = _parse_literal(program)
    assert type(tree) is LiteralNode
    assert tree.type_ == XDType.BOOL
    assert tree.value == value


@pytest.mark.parametrize(
    "program,value",
    [
        ('"c"', "c"),
        ('"x"', "x"),
        ('"0"', "0"),
    ],
)
def test_bool_literal(program, value):
    tree: LiteralNode = _parse_literal(program)
    assert type(tree) is LiteralNode
    assert tree.type_ == XDType.CHAR
    assert tree.value == value


@pytest.mark.parametrize(
    "program,value",
    [
        ('"foooooo"', "foooooo"),
        ('"    "', "    "),
        ('"63"', "63"),
    ],
)
def test_bool_literal(program, value):
    tree: LiteralNode = _parse_literal(program)
    assert type(tree) is LiteralNode
    assert tree.type_ == XDType.STRING
    assert tree.value == value
