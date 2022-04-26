import typer

from xdlang.meta.generate_visitor import generate_visitor

app = typer.Typer()


@app.command()
def visitor():
    print("visitor")
    generate_visitor()


if __name__ == "__main__":
    app()
