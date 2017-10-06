import click

from ambix.migration_home import MigrationHome


@click.command()
@click.argument(
    'alembic-home-dir',
    type=click.Path(exists=True),
)
def flatten(alembic_home_dir):
    home = MigrationHome(alembic_home_dir)
    home.flatten()
