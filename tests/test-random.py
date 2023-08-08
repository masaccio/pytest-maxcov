import random
from collections import namedtuple

Subset = namedtuple("Subset", ["set", "cost"])


def set_cover(universe: set, subsets: list[Subset], confidence: float = 0.9):
    cover_subsets = []
    covered = set()
    cover_subsets = []
    while len(covered) < len(universe) * confidence:
        subset = max(subsets, key=lambda x: len(x.set - covered) / x.cost)
        cover_subsets.append(subset)
        covered |= subset.set

    return cover_subsets


valid_sets = []
all_costs = []
for test_num in range(100):
    max_num = random.randint(10, 100)
    universe = set(range(1, max_num + 1))

    num_sets = random.randint(5, 20)
    subsets = []
    for set_num in range(num_sets):
        num_entries = random.randint(1, 10)
        entries = set(random.sample(list(universe), num_entries))
        subsets.append(
            Subset(
                set=entries,
                cost=max([1, int(sum(entries) * random.random())]),
            )
        )

    elements = set(e for s in subsets for e in s.set)
    if elements == universe:
        valid_sets.append(subsets)

for test_num, subsets in enumerate(valid_sets):
    universe = set(e for s in subsets for e in s.set)
    cover = set_cover(universe, subsets)
    print(
        "universe of {0}-{1} covered by {2} sets from {3} ({4:.1f}%)".format(
            min(universe),
            max(universe),
            len(cover),
            len(subsets),
            100 * (len(cover) / len(subsets)),
        )
    )
