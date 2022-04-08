from hypothesis import given
from hypothesis import strategies as st

from xdlang.xdast import IntLiteralNode


@given(st.integers())
def test_equality(n):
    node1 = IntLiteralNode(n)
    node2 = IntLiteralNode(n)
    assert node1 == node2
    assert not (node1 != node2)


@given(st.integers())
def test_inequality(n):
    node1 = IntLiteralNode(n)
    node2 = IntLiteralNode(n + 1)
    assert node1 != node2
    assert not (node1 == node2)
