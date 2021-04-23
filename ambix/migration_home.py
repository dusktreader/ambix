import pathlib
import typing

import toposort
from ambix.exceptions import AmbixError
from ambix.migration_script import MigrationScript
from ambix.utilities import compose_iters, pairwise


class MigrationHome:
    def __init__(self, home_path: pathlib.Path):
        AmbixError.require_condition(
            home_path.exists(),
            f"migration home path '{home_path}' doesn't exist",
        )
        self.home_path = home_path

        self.migrations = {}
        for migration_file in self.home_path.iterdir():
            if not migration_file.suffix == ".py":
                continue
            script = MigrationScript.parse_file(migration_file)
            self.migrations[script.revision] = script

    def generate_dependency_graph(self):
        return {k: set(compose_iters(v.down_revision)) for (k, v) in self.migrations.items()}

    def flatten(self):
        dependencies = self.generate_dependency_graph()
        flattened = toposort.toposort_flatten(dependencies)
        pairs = pairwise(flattened)
        for (new_down, rev) in pairs:
            self.migrations[rev].change_down_revision(new_down)

    def prune(self, rev: str, leave_migration: bool = False):
        AmbixError.require_condition(
            rev in self.migrations,
            f"Couldn't find a revision for {rev}",
        )
        rev_downs = self.migrations[rev].get_down_revisions()
        for migration in self.migrations.values():
            mig_downs = migration.get_down_revisions()
            if len(mig_downs) == 0:
                continue
            elif rev in mig_downs:
                migration.change_down_revision(*(rev_downs | mig_downs - set([rev])))
        if not leave_migration:
            self.migrations.pop(rev).file_path.unlink()

    def heads(self):
        graph = self.generate_dependency_graph()
        possible_heads = set(graph.keys())
        for down_rev_set in graph.values():
            possible_heads = possible_heads - down_rev_set
        return possible_heads

    def move(self, rev: str, *new_bases: typing.List[str]):
        """
        Moves a single revision to descend from new_bases. Leaves any
        descendant migrations of rev in place by first pruning rev
        """
        if len(new_bases) == 0:
            new_bases = self.heads()
        self.prune(rev, leave_migration=True)
        self.migrations[rev].change_down_revision(*new_bases)

    def ancestors(self, rev: str) -> typing.Iterator[MigrationScript]:
        """
        provides a generator that finds all ancestors of a rev by performing a
        depth-first search
        """
        visited = set()
        yield from self._ancestors(rev, visited)

    def _ancestors(self, rev: str, visited: typing.List[MigrationScript]) -> typing.Iterator[MigrationScript]:
        child = self.migrations[rev]
        parents = child.get_down_revisions()
        for parent in sorted(parents):
            if parent in visited:
                continue
            visited.add(parent)
            yield from self._ancestors(parent, visited=visited)
            yield parent

    def rebase(self, rev: str, *new_bases: typing.List[str]):
        """
        Moves a revision and all of its descendents to be based on new_bases
        """
        AmbixError.require_condition(
            len(new_bases) > 0,
            "At least one new base must be supplied",
        )
        for base in new_bases:
            AmbixError.require_condition(
                rev not in self.ancestors(base),
                f"Cannot rebase. {rev} is an ancestor of new head {base}",
            )
        self.migrations[rev].change_down_revision(*new_bases)
