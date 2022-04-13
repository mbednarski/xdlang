from unittest.mock import Mock

from hypothesis import given
from hypothesis import strategies as st

from xdlang.xd_ast import BinaryOpNode, Node


@given(st.sampled_from(["+", "-", "*", "/"]))
def test_equality(op):
    lhs = Mock(spec=Node)
    rhs = Mock(spec=Node)

    node1 = BinaryOpNode(lhs, op, rhs)
    node2 = BinaryOpNode(lhs, op, rhs)

    assert node1 == node2
    assert not (node1 != node2)


@given(st.sampled_from(["+", "-", "*", "/"]))
def test_inequality_same_op(op):
    lhs1 = Mock(spec=Node)
    rhs1 = Mock(spec=Node)

    lhs2 = Mock(spec=Node)
    rhs2 = Mock(spec=Node)

    node1 = BinaryOpNode(lhs1, op, rhs1)
    node2 = BinaryOpNode(lhs2, op, rhs2)

    assert node1 != node2
    assert not (node1 == node2)
