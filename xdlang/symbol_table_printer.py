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

    scope = symbol_table.root_scope

    for f in scope.functions.values():
        functions.add_row(f.identifier, str(f.type), ', '.join( [f'{x[0]} {x[1]}' for x in f.args]))

    panel = Panel(functions, title="Symbol Table")
    console.print(panel)
