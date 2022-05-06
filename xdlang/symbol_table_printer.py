from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from xdlang.visitors.symbol_table import SymbolTable


def print_symbol_table(symbol_table: SymbolTable) -> None:
    console = Console()

    functions = Table(title="Functions")
    functions.add_column("Identifier", justify="left")
    functions.add_column("Type", justify="left")
    functions.add_column("Arguments", justify="left")

    for f in symbol_table.functions.values():
        functions.add_row(f.identifier, str(f.type), ", ".join(f.args))

    panel = Panel(functions, title="Symbol Table")
    console.print(panel)
