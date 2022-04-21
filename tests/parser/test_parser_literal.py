from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_literal(text):
    return parse_text(program_text=text, start="expr")


@pytest.mark.parametrize("text", ["0", "42", "999999"])
def test_int_literal(text):
    parsed = parse_literal(text)
    assert parsed.children[0].type == "LITERAL"
    assert parsed.children[0].value == text


@pytest.mark.parametrize("text", ["0.0", "4.2", "999.999"])
def test_float_literal(text):
    parsed = parse_literal(text)
    assert parsed is not None
    assert parsed.children[0].type == "LITERAL"
    assert parsed.children[0].value == text


@pytest.mark.parametrize("text", ["'a'", "'x'", "' '"])
def test_char_literal(text):
    parsed = parse_literal(text)
    assert parsed is not None
    assert parsed.children[0].type == "LITERAL"
    assert parsed.children[0].value == text
