from collections import defaultdict
from dataclasses import dataclass

from xdlang.xdtypes import XDType


@dataclass
class Variable:
    identifier: str
    type_: XDType
    var: object
    scope: str


class LookupTable:
    def __init__(self) -> None:
        self.scopes_table = defaultdict(dict)

    def add_variable(self, var: Variable, scope):
        self.scopes_table[scope][var.identifier] = var

    def get_variable(self, identifier: str, scope: str) -> Variable:
        return self.scopes_table[scope][identifier]

    def variable_exists(self, identifier: str, scope: str) -> bool:
        table = self.scopes_table[scope]
        return identifier in table

    def get(self, identifier: str) -> Variable:
        return self.lookup_table[identifier]
