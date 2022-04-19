from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_stmt(text):
    return parse_text(program_text=text, start="statement")


@pytest.mark.parametrize(
    "text,value",
    [
        ("return 42;", "42"),
        ("return 0.0;", "0.0"),
        ("return false;", "false"),
        ("return 'x';", "'x'"),
    ],
)
def test_return_stmt(text, value):
    parsed = parse_stmt(text)
    assert parsed.data.value == "return_stmt"
    assert parsed.children[1].children[0].type == "LITERAL"
    assert parsed.children[1].children[0].value == value
