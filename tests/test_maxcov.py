import pytest
import os


@pytest.mark.script_launch_mode("subprocess")
def test_two_pass(script_runner, tmpdir_test_env):
    ret = script_runner.run(
        ["python3", "-m", "pytest", "--maxcov-record", "--cov-context=test"],
        print_result=False,
    )
    assert ret.stderr == ""
    assert ret.success
    assert os.path.exists(".maxcov")

    ret = script_runner.run(
        ["python3", "-m", "pytest", "--maxcov", "-vvv"],
        print_result=False,
    )
    assert ret.stderr == ""
    assert ret.success
