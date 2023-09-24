from os import chdir, getcwd
from shutil import copytree, rmtree
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture(name="tmpdir_test_env")
def tmpdir_test_env_fixture():
    """Copy tests to a temporary directory, change directory to run the
    test and then change back to the CWD on completion"""

    with TemporaryDirectory() as tmpdir:
        cwd = getcwd()
        rmtree(tmpdir)
        copytree("test_env", tmpdir)
        chdir(tmpdir)
        yield tmpdir

        chdir(cwd)
