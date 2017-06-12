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
        ]

    def test_generate_dependency_graph(self, scripts_dir):
        home = MigrationHome(scripts_dir)
        assert home.generate_dependency_graph() == {
            'aaaaaa': {None},
            'bbbbbb': {'aaaaaa'},
            'cccccc': {'bbbbbb'},
            'dddddd': {'bbbbbb'},
            'eeeeee': {'cccccc', 'dddddd'},
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
        }
