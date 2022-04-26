from llvmlite import ir
from rich import print as rprint

import xdlang.xdtypes as xdtypes

# from xdlang.codegen import LlvmCodeGenerator
from xdlang.parser import parse_text, transform_parse_tree
from xdlang.type_check import TypeChecker

with open("test_programs/type_check.xd", "rt") as f:
    program_text = f.read()

tree = parse_text(program_text)
rprint(tree)

ast = transform_parse_tree(tree)
rprint(ast)


from xd_ast_printer import AstPrinter

from xdlang.symbol_table import SymbolTable

printer = AstPrinter()
printer.visit_program(ast)

printer.print()

symbol_table = SymbolTable()
symbol_table.visit_program(ast)

type_checker = TypeChecker()
type_checker.visit_program(ast)

pass

# code_generator = LlvmCodeGenerator()
# code_generator.generate_runtime()

# ast.accept(code_generator)

# code_generator.generate_epilogue()

# ir_code = code_generator.get_ir_code()
# print(ir_code)

# with open("asdf_module.ll", "wt") as f:
#     f.write(str(ir_code))
