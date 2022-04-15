import xd_ast
from rich import print as rprint
from rich.tree import Tree


class AstPrinter:
    def __init__(self) -> None:
        self.branch_stack = [Tree("xd")]
        self.indent = 0
        pass

    def visit_binary(self, node: xd_ast.BinaryNode):
        print(f'{"  " * self.indent}{node}')
        branch = self.branch_stack[-1].add(str(node))
        self.branch_stack.append(branch)
        node.lhs.accept(self)
        node.rhs.accept(self)
        self.branch_stack.pop()

    def visit_read_var(self, node: xd_ast.ReadVarNode):
        self.branch_stack[-1].add(str(node))

    def visit_literal(self, node: xd_ast.LiteralNode):
        self.branch_stack[-1].add(str(node))

    def print(self):
        rprint(self.branch_stack[0])
