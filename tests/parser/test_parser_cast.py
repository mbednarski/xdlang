from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_expr(text):
    return parse_text(program_text=text, start="expr")


@pytest.mark.parametrize(
    "text,target_type,value",
    [
        ("CAST<int> 0.0", "int", "0.0"),
        ("CAST<float> 0", "float", "0"),
        ("CAST<char> 48", "char", "48"),
        ("CAST<bool> 7", "bool", "7"),
    ],
)
def test_cast_expr(text, target_type, value):
    parsed = parse_expr(text)
    print(parsed.pretty())
    cast = parsed.children[0]
    assert cast.data == "cast_expr"
    assert cast.children[0].type == "IDENTIFIER"
    assert cast.children[0].value == target_type
    assert cast.children[1].type == "LITERAL"
    assert cast.children[1].value == value
