import os
import re
from collections import namedtuple
from typing import List, Set, Union

import pytest
from coverage import CoverageData

Subset = namedtuple("Subset", ["set", "cost", "context"])


def set_cover(
    universe: Set, subsets: List[Subset], confidence: Union[None, float] = None
) -> List[list]:
    remaining_elements = set(e for s in subsets for e in s.set)
    if universe != remaining_elements:
        raise RuntimeError("union of all sets doesn't match universe")

    if confidence is not None and (confidence <= 0.0 or confidence > 1.0):
        raise RuntimeError("subset match confidence must be >0.0 or <=1.0")

    covered = set()
    cover_subsets = []
    while True:
        best_subset = max(subsets, key=lambda x: len(x.set - covered) / x.cost)
        cover_subsets.append(best_subset)
        covered |= best_subset.set

        if confidence is None:
            if len(covered) == len(universe):
                break
        else:
            if len(covered) >= len(universe) * confidence:
                break

    return cover_subsets


context_costs = {}
with open("duration.txt") as fh:
    for line in fh.readlines():
        if " call " not in line:
            continue
        (time, method, context) = line.strip().split()
        context = re.sub(r"[\[\|].*", "", context)
        time = float(time[0:-1])
        context_costs[context] = time

universe = set()
data = CoverageData(".coverage")
root_dir = os.path.dirname(data.base_filename()) + "/"
data.read()
subsets = []
for context in data.measured_contexts():
    if not context:
        continue
    data.set_query_context(context)
    context_func = re.sub(r"[\[\|].*", "", context)
    if data.has_arcs():
        arcs = [
            [f"{filename.replace(root_dir,'')}:{arc}" for arc in data.arcs(filename)]
            for filename in data.measured_files()
        ]
        subset = set(e for s in arcs for e in s)
    else:
        lines = [
            [f"{filename.replace(root_dir,'')}:{line}" for line in data.lines(filename)]
            for filename in data.measured_files()
        ]
        subset = set(e for s in lines for e in s)
    universe |= subset
    if context_func in context_costs:
        cost = context_costs[context_func]
    else:
        cost = 0.001

    subsets.append(Subset(set=subset, cost=cost, context=context_func))

cover_subsets = set_cover(universe, subsets)
contexts = [x.context for x in cover_subsets]
unique_contexts = set()
for context in [x.context for x in cover_subsets]:
    unique_contexts.add(re.sub(r"[\[\|].*", "", context))

print("\n".join(unique_contexts))
