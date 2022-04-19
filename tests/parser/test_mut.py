from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_mut_stmt(text):
    return parse_text(program_text=text, start="mut_stmt")


@pytest.mark.parametrize(
    "text,identifier,value",
    [
        ("mut x = 42;", "x", "42"),
        ("mut y = 0.0;", "y", "0.0"),
        ("mut z = true;", "z", "true"),
        ("mut c = 'x';", "c", "'x'"),
    ],
)
def test_let_stmt(text, identifier, value):
    parsed = parse_mut_stmt(text)
    assert parsed.children[0].type == "IDENTIFIER"
    assert parsed.children[0].value == identifier
    assert parsed.children[1].children[0].type == "LITERAL"
    assert parsed.children[1].children[0].value == value
