import os
import pytest
import shutil

from ambix.utilities import strip_whitespace


@pytest.fixture(scope='session')
def error_matches():
    """
    This fixture provides a function that verifies that an error message
    matches an expected string. Whitespace is stripped from both message and
    string and all case is forced to lower
    """

    def _helper(err_info, compare_string):
        err_string = strip_whitespace(str(err_info.value).lower())
        exp_string = strip_whitespace(str(compare_string).lower())
        if exp_string not in err_string:
            pytest.fail(
                "Expected string '{}' not found in error message '{}'".format(
                    err_info.value, compare_string,
                )
            )
        else:
            return True

    return _helper


@pytest.fixture
def scripts_dir(tmpdir):
    source_dir = os.path.dirname(__file__)

    source_data_dir = os.path.join(source_dir, 'data')
    working_data_dir = os.path.join(str(tmpdir), 'data')
    shutil.copytree(source_data_dir, working_data_dir)

    return working_data_dir
