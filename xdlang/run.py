from llvmlite import ir
from rich import print as rprint

import xdlang.types as xdtypes
from xdlang.parser import parse_text, transform_parse_tree

with open("program.xd", "rt") as f:
    program_text = f.read()

tree = parse_text(program_text)
rprint(tree)

ast = transform_parse_tree(tree)
rprint(ast)

module = ir.Module("asdf")
main_fn = ir.Function(module, xdtypes.main_fn_t, "main")
main_body = main_fn.append_basic_block("entry")
builder = ir.IRBuilder(main_body)

ast.codegen(builder)

print(module)
