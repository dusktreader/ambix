import os
import pytest

from ambix.migration_home import MigrationHome
from ambix.exceptions import AmbixError


class TestMigrationHome:

    def test___init__(self, scripts_dir):
        with pytest.raises(AmbixError) as err_info:
            MigrationHome(home_path='/not/a/valid/path')
        assert "doesn't exist" in str(err_info.value)

        home = MigrationHome(scripts_dir)
        assert home.home_path == scripts_dir
        assert sorted([s for s in home.migrations]) == [
            'aaaaaa',
            'bbbbbb',
            'cccccc',
            'dddddd',
            'eeeeee',
            'ffffff',
            'gggggg',
        ]

    def test_generate_dependency_graph(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'eeeeee': {'cccccc', 'dddddd'},
            'ffffff': {'dddddd'},
            'gggggg': {'eeeeee', 'ffffff'},
        }

    def test_flatten(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        home.flatten()

        assert MigrationHome(scripts_dir).generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'cccccc'},
            'eeeeee': {'dddddd'},
            'ffffff': {'eeeeee'},
            'gggggg': {'ffffff'},
        }

    def test_prune__delete_head(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        assert os.path.exists(os.path.join(
            scripts_dir, 'gggggg-dummy-migration.py'
        ))
        home.prune('gggggg')
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'eeeeee': {'cccccc', 'dddddd'},
            'ffffff': {'dddddd'},
        }
        assert not os.path.exists(os.path.join(
            scripts_dir, 'gggggg-dummy-migration.py'
        ))

    def test_prune__delete_complex_branch(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        assert os.path.exists(os.path.join(
            scripts_dir, 'dddddd-dummy-migration.py'
        ))
        home.prune('dddddd')
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'eeeeee': {'bbbbbb', 'cccccc'},
            'ffffff': {'bbbbbb'},
            'gggggg': {'eeeeee', 'ffffff'},
        }
        assert not os.path.exists(os.path.join(
            scripts_dir, 'dddddd-dummy-migration.py'
        ))

    def test_heads(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        assert home.heads() == {'gggggg'}
        home.prune('gggggg')
        assert home.heads() == {'eeeeee', 'ffffff'}

    def test_rebase__default_new_base(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        home.rebase('eeeeee')
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'ffffff': {'dddddd'},
            'gggggg': {'ffffff', 'cccccc', 'dddddd'},
            'eeeeee': {'gggggg'},
        }

    def test_rebase__specified_new_base(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        home.rebase('eeeeee', 'ffffff')
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'ffffff': {'dddddd'},
            'gggggg': {'ffffff', 'cccccc', 'dddddd'},
            'eeeeee': {'ffffff'},
        }

    def test_rebase__multiple_new_base(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        home.rebase('eeeeee', 'ffffff', 'dddddd')
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'ffffff': {'dddddd'},
            'gggggg': {'ffffff', 'cccccc', 'dddddd'},
            'eeeeee': {'ffffff', 'dddddd'},
        }

    def test_rebase__move_root(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        home.rebase('aaaaaa')
        assert home.generate_dependency_graph() == {
            'bbbbbb': {None},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'eeeeee': {'cccccc', 'dddddd'},
            'ffffff': {'dddddd'},
            'gggggg': {'eeeeee', 'ffffff'},
            'aaaaaa': {'gggggg'},
        }
