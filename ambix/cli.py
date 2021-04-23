import typer
from ambix.commands import flatten, move, prune, rebase, render

cli = typer.Typer()
cli.command()(flatten.flatten)
cli.command()(move.move)
cli.command()(prune.prune)
cli.command()(rebase.rebase)
cli.command()(render.render)
