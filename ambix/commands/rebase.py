import pathlib
import typing

import typer
from ambix.migration_home import MigrationHome


def rebase(
    revision: str = typer.Argument(
        ...,
        help="The revision hash to be moved",
    ),
    alembic_home_dir: pathlib.Path = typer.Option(
        "etc/alembic/versions",
        exists=True,
        help="The directory where the alembic migrations live",
    ),
    new_bases: typing.List[str] = typer.Argument(
        ...,
        help="The new base(s) to base the revision upon",
    ),
):
    home = MigrationHome(alembic_home_dir)
    home.rebase(revision, *new_bases)
