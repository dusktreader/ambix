import pathlib

import typer
from ambix.migration_home import MigrationHome


def flatten(
    alembic_home_dir: pathlib.Path = typer.Option(
        "etc/alembic/versions",
        exists=True,
        help="The directory where the alembic migrations live",
    ),
):
    home = MigrationHome(alembic_home_dir)
    home.flatten()
