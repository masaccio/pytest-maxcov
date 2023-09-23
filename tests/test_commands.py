import pytest
import os
import sys

sys.path = ["."] + sys.path
CWD = os.getcwd()


@pytest.mark.script_launch_mode("inprocess")
def test_help(script_runner):
    os.chdir("dut")

    ret = script_runner.run(["pytest", "--help", "-p", "pytest_maxcov"], print_result=False)
    assert ret.stderr == ""
    assert ret.success

    assert "coverage runtime minimisation" in ret.stdout

    lines = ret.stdout.split("\n")
    for line_num, line in enumerate(lines):
        if line.strip() == "coverage runtime minimisation:":
            break
    lines = lines[line_num + 1 :]
    assert "Run the subset of tests provides maximum coverage" in lines[0]

    os.chdir(CWD)
