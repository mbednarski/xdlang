from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_stmt(text):
    return parse_text(program_text=text, start="statement")


def test_noop_stmt():
    parsed = parse_stmt("NOOP;")
    assert parsed.data.value == "noop_stmt"
