from llvmlite import ir

from xdlang import xd_ast
from xdlang.symbol_table import Symbol
from xdlang.xdtypes import XDType, main_fn_t


class CodeGenerator:
    def __init__(self) -> None:
        self.module = ir.Module("xdapp")
        self.module.triple = "x86_64-pc-linux"
        self.main_fn = ir.Function(self.module, main_fn_t, "main")
        self.main_block = self.main_fn.append_basic_block("main_entry")
        self.builder = ir.IRBuilder(self.main_block)
        self.current_function = self.main_fn

    def get_ir(self):
        return str(self.module)

    def visit_expr(self, node: xd_ast.ExprNode):
        assert False

    def visit_cast(self, node: xd_ast.CastNode):
        source_type = node.expr.type
        target_type = node.type

        value = node.expr.accept(self)

        match (source_type, target_type):
            case (XDType.FLOAT, XDType.INT):
                casted = self.builder.fptosi(value, target_type.get_ir_type())
                return casted
            case _:
                raise Exception("Unsupported cast")

    def visit_stmt(self, node: xd_ast.StmtNode):
        assert False

    def visit_literal(self, node: xd_ast.LiteralNode):
        ir_type = node.type.get_ir_type()
        value = ir.Constant(ir_type, node.value)
        return value

    def visit_binary(self, node: xd_ast.BinaryNode):
        pass

    def visit_unary_neg(self, node: xd_ast.UnaryNegNode):
        match node.type:
            case XDType.FLOAT:
                return self.builder.fneg(node.expr.accept(self))
            case XDType.INT:
                return self.builder.neg(node.expr.accept(self))
            case _:
                assert False

    def visit_read_var(self, node: xd_ast.ReadVarNode):
        var = node.symbol.var
        val = self.builder.load(var)
        return val

    def visit_let_stmt(self, node: xd_ast.LetStmtNode):
        symbol: Symbol = node.symbol
        var = self.builder.alloca(symbol.type.get_ir_type(), 1)
        symbol.var = var
        val = node.expr.accept(self)
        self.builder.store(val, var)

    def visit_mut_stmt(self, node: xd_ast.MutStmtNode):
        pass

    def visit_block(self, node: xd_ast.BlockNode):
        # block = self.current_function.append_basic_block()
        # self.builder.position_at_end(block)
        for stmt in node.statements:
            stmt.accept(self)

    def visit_program(self, node: xd_ast.ProgramNode):
        node.block.accept(self)

    def visit_noop_stmt(self, node: xd_ast.NoopStmtNode):
        pass

    def visit_return_stmt(self, node: xd_ast.ReturnStmtNode):
        value = node.expr.accept(self)
        self.builder.ret(value)
