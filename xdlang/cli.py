import subprocess
from pathlib import Path
from typing import Optional

import typer

from xdlang.compiler import Compiler
from xdlang.meta.generate_visitor import generate_visitor

app = typer.Typer()


def execute_ir(ll_file: Path) -> int:
    """Executes a *.ll file using lli and returns the exit code"""
    proc = subprocess.run(["lli", str(ll_file)], capture_output=True, text=True)

    return proc.returncode


@app.command()
def run(input_file: Path, output_file: Optional[Path] = Path("out.ll")):
    print("XD Compiler")
    print(f"Compiling and running {input_file}")
    compiler = Compiler()
    compiler.compile(input_file, output_file)

    exit_code = execute_ir(output_file)

    print(f"Program returned with code: {exit_code}")


if __name__ == "__main__":
    app()
