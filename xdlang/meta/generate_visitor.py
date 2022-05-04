import ast
from pathlib import Path
from typing import Optional


def generate_visitor(path: Optional[Path] = None):
    print()
    ast_file = Path(__file__).parent.parent / "xd_ast.py"
    tree = ast.parse(ast_file.read_text())

    existing_methods = set()
    if path is not None:
        existing_file = path.read_text()
        existing_tree = ast.parse(existing_file)
        existing_visitor = [
            c for c in existing_tree.body if isinstance(c, ast.ClassDef)
        ][0]
        for method in [
            m for m in existing_visitor.body if isinstance(m, ast.FunctionDef)
        ]:
            existing_methods.add(method.name)

        pass

    nodes = [n for n in tree.body if isinstance(n, ast.ClassDef)]

    expected_methods = set()

    for node in nodes:
        normalized_name = node.name.removesuffix("Node")
        if normalized_name == "":
            continue

        method_name = f"visit"
        for c in normalized_name:
            if c.isupper():
                method_name += "_"
            method_name += c.lower()

        expected_methods.add(method_name)
        if method_name in existing_methods:
            continue

        print(
            f"    def {method_name}(self, node: xd_ast.{node.name}):\n        pass\n\n"
        )

    if existing_methods - expected_methods:
        print("Visitor contains additional methods:")
        print(f"{existing_methods - expected_methods}")
        pass


if __name__ == "__main__":
    generate_visitor(Path("xdlang/symbol_table.py"))
