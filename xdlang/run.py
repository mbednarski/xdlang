from llvmlite import ir
from rich import print as rprint

import xdlang.xdtypes as xdtypes

# from xdlang.codegen import LlvmCodeGenerator
from xdlang.parser import parse_text, transform_parse_tree

with open("test_programs/infix.xd", "rt") as f:
    program_text = f.read()

tree = parse_text(program_text)
rprint(tree)

ast = transform_parse_tree(tree)
rprint(ast)

# code_generator = LlvmCodeGenerator()
# code_generator.generate_runtime()

# ast.accept(code_generator)

# code_generator.generate_epilogue()

# ir_code = code_generator.get_ir_code()
# print(ir_code)

# with open("asdf_module.ll", "wt") as f:
#     f.write(str(ir_code))
