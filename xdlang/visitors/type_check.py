from xdlang import xd_ast
from xdlang.errors import TypeError


class TypeChecker:
    def visit_expr(self, node: xd_ast.ExprNode):
        node.accept(self)

    def visit_cast(self, node: xd_ast.CastNode):
        node.expr.accept(self)
        # TODO: check legal casts
        node.type = node.target_type

    def visit_stmt(self, node: xd_ast.StmtNode):
        pass

    def visit_literal(self, node: xd_ast.LiteralNode):
        pass

    def visit_binary(self, node: xd_ast.BinaryNode):
        node.lhs.accept(self)
        node.rhs.accept(self)
        if node.lhs.type != node.rhs.type:
            if node.lhs.type.can_be_promoted_to(node.rhs.type):
                cast_node = xd_ast.CastNode(
                    line=node.line,
                    column=node.column,
                    target_type=node.rhs.type,
                    expr=node.lhs,
                )
                node.lhs = cast_node
            elif node.rhs.type.can_be_promoted_to(node.lhs.type):
                cast_node = xd_ast.CastNode(
                    line=node.line,
                    column=node.column,
                    target_type=node.lhs.type,
                    expr=node.rhs,
                )
                node.rhs = cast_node
            else:
                raise TypeError(node.line, node.column, node.lhs.type, node.rhs.type)
        node.type = node.lhs.type

    def visit_unary_neg(self, node: xd_ast.UnaryNegNode):
        node.expr.accept(self)
        node.type = node.expr.type
        # if node.expr.type != xd_ast.Type.INT:
        #     raise TypeError(node.line, node.column, node.expr.type, xd_ast.Type.INT)

    def visit_read_var(self, node: xd_ast.ReadVarNode):
        node.type = node.symbol.type

    def visit_let_stmt(self, node: xd_ast.LetStmtNode):
        node.expr.accept(self)
        if node.expr.type != node.type:
            raise Exception(f"Type mismatch: {node.expr.type} != {node.type}")

    def visit_mut_stmt(self, node: xd_ast.MutStmtNode):
        pass

    def visit_block(self, node: xd_ast.BlockNode):
        for stmt in node.statements:
            try:
                stmt.accept(self)
            except TypeError as e:
                print(e.message())

    def visit_program(self, node: xd_ast.ProgramNode):
        node.block.accept(self)

    def visit_noop_stmt(self, node: xd_ast.NoopStmtNode):
        pass

    def visit_return_stmt(self, node: xd_ast.ReturnStmtNode):
        node.expr.accept(self)
