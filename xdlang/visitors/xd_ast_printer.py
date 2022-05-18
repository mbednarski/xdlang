from rich import print as rprint
from rich.tree import Tree

from xdlang.structures import ast
from xdlang.visitors.base_visitor import BaseVisitor


class AstPrinter(BaseVisitor):
    def __init__(self) -> None:
        self.branch_stack = [Tree("xd")]
        self.indent = 0
        pass

    def visit_binary(self, node: ast.BinaryNode):
        branch = self.branch_stack[-1].add(str(node))
        self.branch_stack.append(branch)
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.branch_stack.pop()

    def visit_read_var(self, node: ast.ReadVarNode):
        self.branch_stack[-1].add(str(node))

    def visit_literal(self, node: ast.LiteralNode):
        self.branch_stack[-1].add(str(node))

    def visit_let_stmt(self, node: ast.LetStmtNode):
        branch = self.branch_stack[-1].add(f"let {node.identifier}:{node.type}")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()

    def visit_block(self, node: ast.BlockNode):
        for stmt in node.statements:
            stmt.accept(self)

    def visit_func_definition(self, node: ast.FuncDefinitionNode):
        branch = self.branch_stack[-1].add(
            f"Func {node.identifier}({', '.join( [f'{x[0]} {x[1]}' for x in node.args])}) {node.type}"
        )
        self.branch_stack.append(branch)
        node.body.accept(self)
        self.branch_stack.pop()

    def visit_program(self, node: ast.ProgramNode):
        branch = self.branch_stack[-1].add(f"Program")
        self.branch_stack.append(branch)
        for f in node.functions:
            self.visit_func_definition(f)
        self.branch_stack.pop()

    def visit_mut_stmt(self, node: ast.MutStmtNode):
        branch = self.branch_stack[-1].add(f"mut {node.identifier}")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()

    def print(self):
        rprint(self.branch_stack[0])

    def visit_expr(self, node: ast.ExprNode):
        pass

    def visit_cast(self, node: ast.CastNode):
        branch = self.branch_stack[-1].add(f"Cast<{node.target_type}>")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()

    def visit_stmt(self, node: ast.StmtNode):
        assert False, f"Unhandled StmtNode: {node}"

    def visit_unary_neg(self, node: ast.UnaryNegNode):
        branch = self.branch_stack[-1].add(f"Unary -")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()

    def visit_noop_stmt(self, node: ast.NoopStmtNode):
        self.branch_stack[-1].add(str(node))

    def visit_return_stmt(self, node: ast.ReturnStmtNode):
        branch = self.branch_stack[-1].add(f"Return")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()
