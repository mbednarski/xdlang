from functools import partial

import pytest

from xdlang.parser import parse_text


def parse_expr(text):
    return parse_text(program_text=text, start="expr")


# fmt: off

@pytest.mark.parametrize("text,lhs,op,rhs",
[
    ("42 + 7", '42', '+', '7'),
    ("42 - 7", '42', '-', '7'),
    ("42 * 7", '42', '*', '7'),
    ("42 / 7", '42', '/', '7'),
    ("42 % 7", '42', '%', '7'),
    ("78.4 + 2.78", '78.4', '+', '2.78'),
    ("78.4 - 2.78", '78.4', '-', '2.78'),
    ("78.4 / 2.78", '78.4', '/', '2.78'),
    ("78.4 * 2.78", '78.4', '*', '2.78'),
])
# fmt: on
def test_simple_arithmetic(text, lhs, op, rhs):
    parsed = parse_expr(text)
    assert parsed.data.value == "expr"
    bin_exp = parsed.children[0]
    assert bin_exp.children[0].type == "LITERAL"
    assert bin_exp.children[0].value == lhs
    assert bin_exp.children[1].value == op
    assert bin_exp.children[2].type == "LITERAL"
    assert bin_exp.children[2].value == rhs


def test_operator_priority_arithmetic():
    text = "42 + 7 * 3"
    parsed = parse_expr(text)
    assert parsed.data.value == "expr"
    outer_expr = parsed.children[0]
    assert outer_expr.children[0].type == "LITERAL"
    assert outer_expr.children[1].type == "PLUS"
    assert outer_expr.children[1].value == "+"
    inner_expr = outer_expr.children[2]
    assert inner_expr.data.value == "product"
    assert inner_expr.children[0].type == "LITERAL"
    assert inner_expr.children[0].value == "7"
    assert inner_expr.children[1].type == "STAR"
    assert inner_expr.children[1].value == "*"
    assert inner_expr.children[2].type == "LITERAL"
    assert inner_expr.children[2].value == "3"


def test_parenthesis_arithmetic():
    text = "(42 - 7) * 3"
    parsed = parse_expr(text)
    assert parsed.data.value == "expr"
    outer_expr = parsed.children[0]
    assert outer_expr.children[1].type == "STAR"
    assert outer_expr.children[1].value == "*"
    assert outer_expr.children[2].type == "LITERAL"
    assert outer_expr.children[2].value == "3"
    inner_expr = outer_expr.children[0]
    assert inner_expr.data.value == "sum"
    assert inner_expr.children[0].type == "LITERAL"
    assert inner_expr.children[0].value == "42"
    assert inner_expr.children[1].type == "MINUS"
    assert inner_expr.children[1].value == "-"
    assert inner_expr.children[2].type == "LITERAL"
    assert inner_expr.children[2].value == "7"


def test_unary_arithmetic():
    text = "-42"
    parsed = parse_expr(text)
    assert parsed.data.value == "expr"
    assert parsed.children[0].data == "unary_neg"
    assert parsed.children[0].children[0].type == "LITERAL"
    assert parsed.children[0].children[0].value == "42"


def test_double_minus():
    text = "--42"
    parsed = parse_expr(text)
    assert parsed.data.value == "expr"
    assert parsed.children[0].data == "unary_neg"
    assert parsed.children[0].children[0].data == "unary_neg"
    assert parsed.children[0].children[0].children[0].type == "LITERAL"
    assert parsed.children[0].children[0].children[0].value == "42"
