from pathlib import Path
from typing import Optional

import typer

from xdlang.meta.generate_visitor import generate_visitor

app = typer.Typer()


@app.command()
def visitor(path: Optional[Path]):
    generate_visitor(path)


if __name__ == "__main__":
    app()
