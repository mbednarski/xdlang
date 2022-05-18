from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from xdlang.structures.types import PrimitiveType, TypeBase

from xdlang.structures import XDType, ast


@dataclass
class Symbol:
    type: XDType
    identifier: str
    var: Optional[Any] = None


@dataclass
class Function:
    identifier: str
    type: str
    args: List[Tuple[str, str]]


@dataclass
class Scope:
    parent:  Optional["Scope"]= field(default=None)
    children: List["Scope"] = field(default_factory=list)
    types: dict[str, TypeBase]= field(default_factory=dict)
    functions: dict[str, Function]= field(default_factory=dict)

class SymbolTable:
    def __init__(self) -> None:
        self.root_scope = Scope()
        self.root_scope.types['int'] = PrimitiveType("int")
        self.root_scope.types['bool'] = PrimitiveType("bool")
        self.root_scope.types['float'] = PrimitiveType("float")
        self.root_scope.types['char'] = PrimitiveType("char")

        self.scopes = [self.root_scope]
    

    def insert_function(self, function: Function):        
        scope = self.peek_scope()
        if function.identifier in scope.functions:
            raise Exception(f"Function {function.identifier} already defined")
        scope.functions[function.identifier] = function

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
        for f in node.functions:
            self.visit_function_definition(f)

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

    def visit_function_definition(self, node: ast.FuncDefinitionNode):
        f = Function(node.identifier, node.type, node.args)
        self.insert_function(f)
