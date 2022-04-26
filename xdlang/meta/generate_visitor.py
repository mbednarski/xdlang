import ast
from pathlib import Path


def generate_visitor():
    ast_file = Path(__file__).parent.parent / "xd_ast.py"
    tree = ast.parse(ast_file.read_text())

    nodes = [n for n in tree.body if isinstance(n, ast.ClassDef)]

    for node in nodes:
        normalized_name = node.name.removesuffix("Node")
        if normalized_name == "":
            continue

        method_name = f"visit"
        for c in normalized_name:
            if c.isupper():
                method_name += "_"
            method_name += c.lower()

        print(f"def {method_name}(self, node: xd_ast.{node.name}):\n\tpass\n\n")


if __name__ == "__main__":
    generate_visitor()
