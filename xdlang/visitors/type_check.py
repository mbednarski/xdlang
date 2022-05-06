from xdlang.structures import TypeError, ast


class TypeChecker:
    def visit_expr(self, node: ast.ExprNode):
        node.accept(self)

    def visit_cast(self, node: ast.CastNode):
        node.expr.accept(self)
        # TODO: check legal casts
        node.type = node.target_type

    def visit_stmt(self, node: ast.StmtNode):
        pass

    def visit_literal(self, node: ast.LiteralNode):
        pass

    def visit_binary(self, node: ast.BinaryNode):
        node.lhs.accept(self)
        node.rhs.accept(self)
        if node.lhs.type != node.rhs.type:
            if node.lhs.type.can_be_promoted_to(node.rhs.type):
                cast_node = ast.CastNode(
                    line=node.line,
                    column=node.column,
                    target_type=node.rhs.type,
                    expr=node.lhs,
                )
                node.lhs = cast_node
            elif node.rhs.type.can_be_promoted_to(node.lhs.type):
                cast_node = ast.CastNode(
                    line=node.line,
                    column=node.column,
                    target_type=node.lhs.type,
                    expr=node.rhs,
                )
                node.rhs = cast_node
            else:
                raise TypeError(node.line, node.column, node.lhs.type, node.rhs.type)
        node.type = node.lhs.type

    def visit_unary_neg(self, node: ast.UnaryNegNode):
        node.expr.accept(self)
        node.type = node.expr.type
        # if node.expr.type != ast.Type.INT:
        #     raise TypeError(node.line, node.column, node.expr.type, ast.Type.INT)

    def visit_read_var(self, node: ast.ReadVarNode):
        node.type = node.symbol.type

    def visit_let_stmt(self, node: ast.LetStmtNode):
        node.expr.accept(self)
        if node.expr.type != node.type:
            raise Exception(f"Type mismatch: {node.expr.type} != {node.type}")

    def visit_mut_stmt(self, node: ast.MutStmtNode):
        pass

    def visit_block(self, node: ast.BlockNode):
        for stmt in node.statements:
            try:
                stmt.accept(self)
            except TypeError as e:
                print(e.message())

    def visit_program(self, node: ast.ProgramNode):
        node.block.accept(self)

    def visit_noop_stmt(self, node: ast.NoopStmtNode):
        pass

    def visit_return_stmt(self, node: ast.ReturnStmtNode):
        node.expr.accept(self)
