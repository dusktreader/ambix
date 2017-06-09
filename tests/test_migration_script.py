import os
import pytest
import re

from ambix.migration_script import MigrationScript
from ambix.exceptions import AmbixError


class TestMigrationScript:

    def test_parse_file(self, scripts_dir):
        root_migration = MigrationScript.parse_file(
            os.path.join(scripts_dir, 'aaaaaa-dummy-migration.py')
        )
        assert root_migration.revision == 'aaaaaa'
        assert root_migration.down_revision is None

        root_migration = MigrationScript.parse_file(
            os.path.join(scripts_dir, 'bbbbbb-dummy-migration.py')
        )
        assert root_migration.revision == 'bbbbbb'
        assert root_migration.down_revision == 'aaaaaa'

        with pytest.raises(AmbixError):
            root_migration = MigrationScript.parse_file(
                os.path.join(scripts_dir, 'nonexisting-migration.py')
            )

    def test_change_down_revision(self, scripts_dir):
        script_path = os.path.join(scripts_dir, 'aaaaaa-dummy-migration.py')
        migration = MigrationScript.parse_file(script_path)
        migration.change_down_revision('cccccc')
        assert migration.down_revision == 'cccccc'
        with open(script_path) as script_file:
            contents = script_file.read()
        assert re.search(
            r"down_revision\s*=\s*'cccccc'",
            contents,
            flags=re.MULTILINE,
        )
        assert re.search(
            r'Revises:\s*cccccc',
            contents,
            flags=re.MULTILINE,
        )

        script_path = os.path.join(scripts_dir, 'bbbbbb-dummy-migration.py')
        migration = MigrationScript.parse_file(script_path)
        migration.change_down_revision('cccccc')
        assert migration.down_revision == 'cccccc'
        with open(script_path) as script_file:
            contents = script_file.read()
        assert re.search(
            r'Revises:\s*cccccc',
            contents,
            flags=re.MULTILINE,
        )
        assert re.search(
            r"down_revision\s*=\s*'cccccc'",
            contents,
            flags=re.MULTILINE,
        )

        script_path = os.path.join(scripts_dir, 'cccccc-dummy-migration.py')
        migration = MigrationScript.parse_file(script_path)
        migration.change_down_revision('aaaaaa', 'bbbbbb')
        assert migration.down_revision == ('aaaaaa', 'bbbbbb')
        with open(script_path) as script_file:
            contents = script_file.read()
        assert re.search(
            r'Revises:\s*aaaaaa, bbbbbb',
            contents,
            flags=re.MULTILINE,
        )
        assert re.search(
            r"down_revision\s*=\s*\('aaaaaa', 'bbbbbb'\)",
            contents,
            flags=re.MULTILINE,
        )

        script_path = os.path.join(scripts_dir, 'eeeeee-dummy-migration.py')
        migration = MigrationScript.parse_file(script_path)
        migration.change_down_revision('aaaaaa')
        assert migration.down_revision == 'aaaaaa'
        with open(script_path) as script_file:
            contents = script_file.read()
        assert re.search(
            r'Revises:\s*aaaaaa',
            contents,
            flags=re.MULTILINE,
        )
        assert re.search(
            r"down_revision\s*=\s*'aaaaaa'",
            contents,
            flags=re.MULTILINE,
        )
