from dataclasses import dataclass
from typing import Any, List, Optional

from xdlang.structures import XDType, ast


@dataclass
class Symbol:
    type: XDType
    identifier: str
    var: Optional[Any] = None


@dataclass
class Scope:
    parent: Optional["Scope"]
    symbols: dict
    name: str


class SymbolTable:
    def __init__(self) -> None:
        self.scopes: List[Scope] = [Scope(None, {}, "ROOT")]

    def push_scope(self, name: str) -> dict:
        scope = Scope(parent=self.scopes[-1], symbols={}, name=name)
        self.scopes.append(scope)
        return scope

    def pop_scope(self):
        self.scopes.pop()

    def peek_scope(self):
        return self.scopes[-1]

    def insert_symbol(self, symbol: Symbol):
        # if already defined in current scope, raise an error
        if symbol.identifier in self.scopes[-1].symbols:
            raise Exception(
                f"Symbol {symbol.identifier} already defined in current scope"
            )

        self.scopes[-1].symbols[symbol.identifier] = symbol

    def get_symbol(self, identifier: str, scope: Scope):
        while scope.parent != None:
            if identifier in scope.symbols:
                return scope.symbols[identifier]
            scope = scope.parent
        raise Exception(f"Symbol {identifier} not found")

    def visit_program(self, node: ast.ProgramNode):
        self.visit_block(node.block)

    def visit_block(self, node: ast.BlockNode):
        self.push_scope("block")
        for stmt in node.statements:
            stmt.accept(self)
        self.pop_scope()

    def visit_let_stmt(self, node: ast.LetStmtNode):
        symbol = Symbol(node.type, node.identifier)
        self.insert_symbol(
            symbol,
        )
        node.symbol = symbol

    def visit_noop_stmt(self, node: ast.NoopStmtNode):
        pass

    def visit_return_stmt(self, node: ast.ReturnStmtNode):
        node.expr.accept(self)

    def visit_mut_stmt(self, node: ast.MutStmtNode):
        symbol = self.get_symbol(node.identifier, self.scopes[-1])
        node.symbol = symbol

    def visit_read_var(self, node: ast.ReadVarNode):
        symbol = self.get_symbol(node.identifier, self.scopes[-1])
        node.symbol = symbol

    def visit_cast(self, node: ast.CastNode):
        node.expr.accept(self)

    def visit_unary_neg(self, node: ast.UnaryNegNode):
        node.expr.accept(self)

    def visit_literal(self, node: ast.LiteralNode):
        pass
