import pathlib
import shutil

import pytest


@pytest.fixture
def scripts_dir(tmp_path):
    source_dir = pathlib.Path(__file__).parent
    source_data_dir = source_dir / "data"

    working_data_dir = tmp_path / "data"
    shutil.copytree(source_data_dir, working_data_dir)

    return working_data_dir
