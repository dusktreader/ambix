import os
import toposort

from ambix.exceptions import AmbixError
from ambix.migration_script import MigrationScript
from ambix.utilities import compose_iters, pairwise


class MigrationHome:

    def __init__(self, home_path):
        AmbixError.require_condition(
            os.path.exists(home_path),
            "migration home path '{}' doesn't exist",
            home_path,
        )
        self.home_path = home_path

        self.migrations = {}
        for migration_file in os.listdir(self.home_path):
            if not migration_file.endswith('.py'):
                continue
            script = MigrationScript.parse_file(os.path.join(
                self.home_path,
                migration_file,
            ))
            self.migrations[script.revision] = script

    def generate_dependency_graph(self):
        return {
            k: set(compose_iters(v.down_revision))
            for (k, v) in self.migrations.items()
        }

    def flatten(self):
        dependencies = self.generate_dependency_graph()
        flattened = toposort.toposort_flatten(dependencies)
        pairs = pairwise(flattened)
        for (new_down, rev) in pairs:
            self.migrations[rev].change_down_revision(new_down)

    def prune(self, rev, leave_migration=False):
        AmbixError.require_condition(
            rev in self.migrations,
            "Couldn't find a revision for {}",
            rev,
        )
        rev_downs = self.migrations[rev].get_down_revisions()
        for migration in self.migrations.values():
            mig_downs = migration.get_down_revisions()
            if len(mig_downs) == 0:
                continue
            elif rev in mig_downs:
                migration.change_down_revision(
                    *(rev_downs | mig_downs - set([rev]))
                )
        if not leave_migration:
            os.remove(self.migrations[rev].file_path)
            del self.migrations[rev]

    def heads(self):
        graph = self.generate_dependency_graph()
        possible_heads = set(graph.keys())
        for down_rev_set in graph.values():
            possible_heads = possible_heads - down_rev_set
        return possible_heads

    def move(self, rev, *new_bases):
        """
        Moves a single revision to descend from new_bases. Leaves any
        descendant migrations of rev in place by first pruning rev
        """
        if len(new_bases) == 0:
            new_bases = self.heads()
        self.prune(rev, leave_migration=True)
        self.migrations[rev].change_down_revision(*new_bases)

    def ancestors(self, rev):
        """
        provides a generator that finds all ancestors of a rev by performing a
        depth-first search
        """
        visited = set()
        yield from self._ancestors(rev, visited)

    def _ancestors(self, rev, visited):
        child = self.migrations[rev]
        parents = child.get_down_revisions()
        for parent in sorted(parents):
            if parent in visited:
                continue
            visited.add(parent)
            yield from self._ancestors(parent, visited=visited)
            yield parent

    def rebase(self, rev, *new_bases):
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
                "Cannot rebase.  {} is an ancestor of new head {}",
                rev, base,
            )
        self.migrations[rev].change_down_revision(*new_bases)
