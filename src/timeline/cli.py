"""CLI 入口"""

import typer
from . import __version__

app = typer.Typer(
    name="dong-timeline",
    help="时间咚 - 记录人生/项目的关键节点",
)

# 导入命令
from .commands import init, add, ls, get, update, delete, stats, search

app.command()(init.init)
app.command()(add.add)
app.command(name="list")(ls.list_events)
app.command()(get.get)
app.command()(update.update)
app.command()(delete.delete)
app.command()(stats.stats)
app.command()(search.search)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="显示版本"),
):
    """时间咚 - 记录人生/项目的关键节点"""
    if version:
        from rich.console import Console
        console = Console()
        console.print(f"dong-timeline {__version__}")
        raise typer.Exit()


