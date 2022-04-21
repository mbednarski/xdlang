import pytest

from xdlang.parser import parse_text


def parse_block(text):
    return parse_text(program_text=text, start="block")


def test_int_literal():
    text = """{
noop;
noop;
noop;
}"""
    parsed = parse_block(text)
    print(parsed.children[1])
    assert parsed.data.value == "block"
    assert parsed.children[1].data == "noop_stmt"
    assert parsed.children[2].data == "noop_stmt"
    assert parsed.children[3].data == "noop_stmt"
