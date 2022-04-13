import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from xdlang.parser import parse_text, transform_parse_tree
from xdlang.xd_ast import BinaryOpNode, IntLiteralNode


@given(
    st.integers(),
    st.text(alphabet=" \t\n"),
    st.sampled_from(["+", "-", "/", "*"]),
    st.text(alphabet=" \t\n"),
    st.integers(),
)
def test_binary_expr_int(lhs, sep1, op, sep2, rhs):
    print(lhs, op, rhs)
    text = f"{lhs}{sep1}{op}{sep2}{rhs}"
    parsed = parse_text(text, start="expr")
    transformed = transform_parse_tree(parsed)

    assert transformed == BinaryOpNode(IntLiteralNode(lhs), op, IntLiteralNode(rhs))
