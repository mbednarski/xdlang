from pathlib import Path

from llvmlite import ir
from rich import print as rprint
from rich.panel import Panel

import xdlang.xdtypes as xdtypes

# from xdlang.codegen import LlvmCodeGenerator
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.symbol_table import SymbolTable
from xdlang.type_check import TypeChecker
from xdlang.visitors.code_generator import CodeGenerator
from xdlang.visitors.xd_ast_printer import AstPrinter
from xdlang.xd_ast import ProgramNode


class Compiler:
    def __init__(self) -> None:
        self.ast_printer = AstPrinter()
        self.symbol_table = SymbolTable()
        self.type_checker = TypeChecker()
        self.code_generator = CodeGenerator()

    def compile(self, input_file: Path, target_file: Path) -> None:
        with input_file.open("rt") as f:
            program_text = f.read()

        parse_tree = parse_text(program_text)

        rprint(Panel(parse_tree, title="Parse Tree"))

        ast_tree = transform_parse_tree(parse_tree)
        self.ast_printer.visit_program(ast_tree)
        rprint(Panel(self.ast_printer.branch_stack[0], title="AST Tree"))

        # self.symbol_table.visit_program(ast_tree)
        # self.type_checker.visit_program(ast_tree)
        # self.code_generator.visit_program(ast_tree)

        # with target_file.open("wt") as f:
        #     f.write(self.code_generator.get_ir())


# with open("test_programs/simple_return.xd", "rt") as f:
#     program_text = f.read()

# tree = parse_text(program_text)
# rprint(tree)

# ast: ProgramNode = transform_parse_tree(tree)
# rprint(ast)


# printer.visit_program(ast)

# printer.print()

# symbol_table = SymbolTable()
# symbol_table.visit_program(ast)

# type_checker = TypeChecker()
# type_checker.visit_program(ast)

# printer = AstPrinter()
# printer.visit_program(ast)

# printer.print()

# codegen = CodeGenerator()
# codegen.visit_program(ast)

# print(codegen.get_ir())

# with open("out.ir", "wt") as f:
#     f.write(codegen.get_ir())

# pass
