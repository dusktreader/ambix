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

    def prune(self, rev):
        AmbixError.require_condition(
            rev in self.migrations,
            "Couldn't find a revision for {}",
            rev,
        )
        new_down = self.migrations[rev].down_revision
        for migration in self.migrations.values():
            if migration.down_revision is None:
                continue
            elif rev == migration.down_revision:
                migration.change_down_revision(new_down)
            elif rev in migration.down_revision:
                migration.change_down_revision(
                    [dr for dr in migration.down_revision if dr != rev]
                )
        os.remove(self.migrations[rev].file_path)
        del self.migrations[rev]
