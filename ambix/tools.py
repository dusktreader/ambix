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


@click.command()
@click.argument(
    'alembic-home-dir',
    type=click.Path(exists=True),
)
@click.argument(
    'revision',
)
def prune(alembic_home_dir, revision):
    home = MigrationHome(alembic_home_dir)
    home.prune(revision)


@click.command()
@click.argument(
    'alembic-home-dir',
    type=click.Path(exists=True),
)
@click.argument(
    'revision',
)
@click.argument(
    'new_bases',
    nargs=-1,
)
def rebase(alembic_home_dir, revision, new_bases):
    home = MigrationHome(alembic_home_dir)
    home.rebase(revision, *new_bases)
