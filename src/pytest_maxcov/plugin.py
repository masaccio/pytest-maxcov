# import os
# import re
from collections import namedtuple, defaultdict
from typing import List, Set, Union

import coverage
import pytest
import time
from coverage import CoverageData


def pytest_addoption(parser):
    parser.addoption(
        "--maxcov",
        action="store_true",
        default=False,
        help=(
            "Run the subset of tests provides maximum coverage with the minimum"
            "execution time. Requires a previous pytest run using --maxcov-record"
        ),
    )
    parser.addoption(
        "--maxcov-record",
        action="store_true",
        default=False,
        help="Record coverage and timing data for the --maxcov option",
    )
    parser.addoption(
        "--maxcov-threshold",
        type=float,
        default=100.0,
        help="Set the threshold for computing maximum coverage. Default: 100.0",
    )


def pytest_configure(config):
    config.pluginmanager.register(MaxCovPlugin(config), "maxcov-plugin")


class TestDuration:
    def __init__(self):
        self.start = None
        self.end = None

    @property
    def delta(self) -> time:
        return self.end - self.start


class MaxCovPlugin:
    def __init__(self, config):
        self.config = config
        self.durations = defaultdict(TestDuration)

    def pytest_collection_modifyitems(self, items, config):
        if not config.option.maxcov:
            return
        durations = {}
        lineno = 1
        try:
            fh = open(".maxcov", "r")
        except FileNotFoundError as e:
            raise pytest.UsageError(str(e)) from e

        for line in fh.readlines():
            try:
                (nodeid, delta) = line.split("=")
                durations[nodeid] = delta
            except Exception as e:
                raise pytest.UsageError(f".maxcov is corrupted at line {lineno}") from e
            lineno += 1

    def pytest_runtest_logstart(self, nodeid, location):
        if self.config.option.maxcov_record:
            self.durations[nodeid].start = time.time()

    def pytest_runtest_logfinish(self, nodeid, location):
        if self.config.option.maxcov_record:
            self.durations[nodeid].end = time.time()

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int):
        if self.config.option.maxcov_record:
            with open(".maxcov", "w") as fh:
                for nodeid, duration in self.durations.items():
                    print(f"{nodeid}={duration.delta}", file=fh)


# def set_cover(
#     universe: Set, subsets: List[Subset], confidence: Union[None, float] = None
# ) -> List[list]:
#     all_elements = set(e for s in subsets for e in s.set)
#     if universe != all_elements:
#         raise RuntimeError("union of all sets doesn't match universe")

#     if confidence is not None and (confidence <= 0.0 or confidence > 1.0):
#         raise RuntimeError("subset match confidence must be >0.0 and <=1.0")

#     covered = set()
#     cover_subsets = []
#     while True:
#         best_subset = max(subsets, key=lambda x: len(x.set - covered) / x.cost)
#         cover_subsets.append(best_subset)
#         covered |= best_subset.set

#         if confidence is None:
#             if len(covered) == len(universe):
#                 break
#         else:
#             if len(covered) >= len(universe) * confidence:
#                 break

#     return cover_subsets


# context_costs = {}
# with open("duration.txt") as fh:
#     for line in fh.readlines():
#         if " call " not in line:
#             continue
#         (time, method, context) = line.strip().split()
#         context = re.sub(r"[\[\|].*", "", context)
#         time = float(time[0:-1])
#         context_costs[context] = time

# universe = set()
# data = CoverageData(".coverage")
# root_dir = os.path.dirname(data.base_filename()) + "/"
# data.read()
# subsets = []
# for context in data.measured_contexts():
#     if not context:
#         continue
#     data.set_query_context(context)
#     context_func = re.sub(r"[\[\|].*", "", context)
#     if data.has_arcs():
#         arcs = [
#             [f"{filename.replace(root_dir,'')}:{arc}" for arc in data.arcs(filename)]
#             for filename in data.measured_files()
#         ]
#         subset = set(e for s in arcs for e in s)
#     else:
#         lines = [
#             [f"{filename.replace(root_dir,'')}:{line}" for line in data.lines(filename)]
#             for filename in data.measured_files()
#         ]
#         subset = set(e for s in lines for e in s)
#     universe |= subset
#     if context_func in context_costs:
#         cost = context_costs[context_func]
#     else:
#         cost = 0.001

#     subsets.append(Subset(set=subset, cost=cost, context=context_func))

# cover_subsets = set_cover(universe, subsets)
# unique_contexts = [x.context for x in cover_subsets]

# print("\n".join(unique_contexts))
