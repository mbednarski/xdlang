from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_let_stmt(text):
    return parse_text(program_text=text, start="statement")


@pytest.mark.parametrize(
    "text,type,identifier,value",
    [
        ("let int x = 42;", "int", "x", "42"),
        ("let float y = 0.0;", "float", "y", "0.0"),
        ("let bool z = true;", "bool", "z", "true"),
        ("let char c = 'x';", "char", "c", "'x'"),
    ],
)
def test_let_stmt(text, type, identifier, value):
    parsed = parse_let_stmt(text)
    print(parsed.pretty())
    assert parsed.children[0].type == "IDENTIFIER"
    assert parsed.children[0].value == type
    assert parsed.children[1].type == "IDENTIFIER"
    assert parsed.children[1].value == identifier
    assert parsed.children[2].children[0].type == "LITERAL"
    assert parsed.children[2].children[0].value == value
