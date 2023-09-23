sys.path = ["."] + sys.path
CWD = os.getcwd()
print(">>>", sys.path, "<<<")

import pytest
import os
import sys


@pytest.mark.script_launch_mode("subprocess")
def test_help(script_runner):
    os.chdir("tests/dut")

    ret = script_runner.run(["pytest", "--help", "-p", "pytest_maxcov"], print_result=False)
    assert ret.stderr == ""
    assert ret.success

    assert "coverage runtime minimisation" in ret.stdout

    for line in ret.stdout.split("\r\n"):
        if line.strip() == "coverage runtime minimisation":
            break

    lines = [x.strip() for x in ret.stdout.split("\r\n")]
    assert "Run the subset of tests provides maximum coverage" in lines[0]
    assert "Record coverage and timing data for the --maxcov option" in lines[1]
    assert "Set the threshold for computing maximum coverage. Default: 100.0" in lines[2]

    os.chdir(CWD)
