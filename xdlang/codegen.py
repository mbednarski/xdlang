from logging import getLogger

from llvmlite import ir

from xdlang.lookup_table import LookupTable, Variable
from xdlang.xdast import (
    BinaryOpNode,
    GetVariableNode,
    IfStmtNode,
    LetStmtNode,
    LiteralNode,
    MutStmtNode,
    ProgramNode,
)
from xdlang.xdtypes import XDType, main_fn_t

logger = getLogger(__name__)


class LlvmCodeGenerator:
    def __init__(self) -> None:
        self.module = ir.Module("xdmodule")
        self.module.triple = "x86_64-pc-linux"
        self.main_fn = ir.Function(self.module, main_fn_t, "main")
        self.main_body = self.main_fn.append_basic_block("main_entry")
        self.builder: ir.IRBuilder = ir.IRBuilder(self.main_body)

        self.lookup_table = LookupTable()

    def generate_runtime(self):
        int32_t = XDType.INT.get_ir_type()
        putchar_t = ir.FunctionType(int32_t, (int32_t,))
        putchar_func = ir.Function(self.module, putchar_t, "putchar")

    def generate_epilogue(self):
        self.builder.ret(ir.IntType(64)(0))

    def get_ir_code(self):
        return str(self.module)

    def visit_program(self, node: ProgramNode):
        pass

    def visit_block(self, block: ProgramNode):
        pass

    def visit_let_stmt(self, stmt: LetStmtNode, expr_val):
        # check of variable already exists in current scope
        scope = "main"

        if self.lookup_table.variable_exists(stmt.identifier, scope=scope):
            raise TypeError(
                f"Variable {stmt.identifier} already exists in scope {scope}"
            )

        allocated = self.builder.alloca(
            stmt.type_.get_ir_type(), 1, name=stmt.identifier
        )
        var = Variable(stmt.identifier, stmt.type_, allocated, scope=scope)
        self.lookup_table.add_variable(var, scope=scope)

        stored = self.builder.store(expr_val, allocated)

    def visit_literal(self, literal: LiteralNode):
        if literal.type_ == XDType.CHAR:
            return ir.Constant(literal.type_.get_ir_type(), ord(literal.value))

        return ir.Constant(literal.type_.get_ir_type(), literal.value)

    def visit_binary_op(self, node: BinaryOpNode, lval, rval):

        match (node.op, node.type_):
            case ("+", XDType.INT):
                retval = self.builder.add(lval, rval)
            case _:
                assert False

        return retval

    def visit_get_variable(self, node: GetVariableNode):
        scope = "main"
        var = self.lookup_table.get_variable(node.identifier, scope=scope)
        return self.builder.load(var.var)

    def visit_mut_stmt(self, node: MutStmtNode, expr_val):
        scope = "main"
        if not self.lookup_table.variable_exists(node.identifier, scope=scope):
            raise TypeError(f"Variable {node.identifier} does not exist")

        var = self.lookup_table.get_variable(node.identifier, scope=scope)
        if var.type_ != node.expr.type_:
            raise TypeError(
                "Variable {} is of type {}, but expression is of type {}".format(
                    node.identifier, var.type_, node.expr.type_
                )
            )

        self.builder.store(expr_val, var.var)

    def visit_if_stmt(self, node: IfStmtNode, condition_code, if_code, else_code):
        evaluated_condition = node.condition.accept(self)
        with self.builder.if_else(evaluated_condition) as (then, otherwise):
            with then:
                node.if_block.accept(self)
            if node.else_block is not None:
                with otherwise:
                    node.else_block.accept(self)


class XDException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
