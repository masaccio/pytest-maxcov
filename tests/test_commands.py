import pytest


@pytest.mark.script_launch_mode("subprocess")
def test_command_line(script_runner, tmpdir_test_env):
    ret = script_runner.run(["pytest", "--help"], print_result=False)
    assert ret.stderr == ""
    assert ret.success

    assert "coverage runtime minimisation" in ret.stdout


@pytest.mark.script_launch_mode("subprocess")
def test_command_line_errors(script_runner, tmpdir_test_env):
    ret = script_runner.run(["pytest", "--maxcov-threshold=0.0"], print_result=False)
    assert "--maxcov-threshold must be >0.0 and <=100.0" in ret.stderr
    assert not ret.success

    ret = script_runner.run(["pytest", "--maxcov-threshold=101"], print_result=False)
    assert "--maxcov-threshold must be >0.0 and <=100.0" in ret.stderr
    assert not ret.success

    ret = script_runner.run(["pytest", "--maxcov", "--no-cov"], print_result=False)
    assert "disabled with --no-cov" in ret.stderr
    assert not ret.success
