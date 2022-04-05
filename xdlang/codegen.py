from logging import getLogger

from llvmlite import ir

import xdlang.types as xdtypes

logger = getLogger(__name__)

class LlvmCodeGenerator:
    def __init__(self) -> None:
        self.module = ir.Module('asdf')
        self.main_fn = ir.Function(self.module, xdtypes.main_fn_t, 'main')
        self.main_body = self.main_fn.append_basic_block('entry')
        self.builder = ir.IRBuilder(self.main_body)

    def generate(self, program) -> None:
        pass

    def generate_program(self, program_node):        
        for exp in self.expressions:
            exp.codegen(self.)

    def generate_expr(self, expr):
        pass

    def generate_let_stmt(self, let_stmt):
        pass