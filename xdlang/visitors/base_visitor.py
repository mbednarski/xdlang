from xdlang.structures import ast


class BaseVisitor:
    def visit_program(self, node: ast.ProgramNode):
        raise NotImplementedError()

    def visit_block(self, node: ast.BlockNode):
        raise NotImplementedError()

    def visit_func_definition(self, node: ast.FuncDefinitionNode):
        raise NotImplementedError()

    def visit_literal(self, node: ast.LiteralNode):
        raise NotImplementedError()
