import pathlib

import typer
from ambix.migration_home import MigrationHome


def render(
    alembic_home_dir: pathlib.Path = typer.Option(
        "etc/alembic/versions",
        exists=True,
        help="The directory where the alembic migrations live",
    ),
):
    home = MigrationHome(alembic_home_dir)
    graph = home.generate_dependency_graph()
    print("strict digraph {")
    for (key, value) in graph.items():
        for child in value:
            if child is None:
                continue
            print(f"  {key} -> {child}")
    print("}")
