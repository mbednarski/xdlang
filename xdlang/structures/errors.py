import xdlang.structures.types as types


class XdError(Exception):
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


class TypeError(XdError):
    def __init__(self, line: int, column: int, lhs: types.XDType, rhs: types.XDType):
        super().__init__(line, column)
        self.lhs = lhs
        self.rhs = rhs

    def message(self):
        return f"{self.line}:{self.column} Type mismatch: {self.lhs} and {self.rhs}"
