import xd_ast
from rich import print as rprint
from rich.tree import Tree


class AstPrinter:
    def __init__(self) -> None:
        self.branch_stack = [Tree("xd")]
        self.indent = 0
        pass

    def visit_binary(self, node: xd_ast.BinaryNode):
        branch = self.branch_stack[-1].add(str(node))
        self.branch_stack.append(branch)
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.branch_stack.pop()

    def visit_read_var(self, node: xd_ast.ReadVarNode):
        self.branch_stack[-1].add(str(node))

    def visit_literal(self, node: xd_ast.LiteralNode):
        self.branch_stack[-1].add(str(node))

    def visit_let_stmt(self, node: xd_ast.LetStmtNode):
        branch = self.branch_stack[-1].add(f"let {node.identifier}:{node.type}")
        self.branch_stack.append(branch)
        node.expr.accept(self)
        self.branch_stack.pop()

    def visit_block(self, node: xd_ast.BlockNode):
        for stmt in node.statements:
            stmt.accept(self)

    def visit_program(self, node: xd_ast.ProgramNode):
        self.visit_block(node.block)

    def print(self):
        rprint(self.branch_stack[0])
