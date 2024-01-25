from lib import *
from wp1 import *


def generate_weights_full(relations, distributions):
    weighted_relations = {1: [], 0: [], "d": []}

    weighted_relations[1] = generate_weights(
        relations[1], distributions[1][0], distributions[1][1], True
    )
    weighted_relations[0] = generate_weights(
        relations[0], distributions[0][0], distributions[0][1], True
    )
    weighted_relations["d"] = generate_weights(
        relations["d"], distributions["d"][0], distributions["d"][1], False
    )

    return weighted_relations


def bipartition(nodeset):
    if len(nodeset) < 2:
        return [nodeset, []]

    random.shuffle(nodeset)

    midpoint = len(nodeset) // 2

    return [nodeset[:midpoint], nodeset[midpoint:]]


if __name__ == "__main__":
    # generate fitch graph based on xenology dataset
    xenology = generate_xenology(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14"
    )

    relations = xenology["relations"]

    # define distribution parameters for generating weights
    distributions = {
        1: (random.uniform, [1.0, 1.5]),
        0: (random.random, []),
        "d": (random.uniform, [1.0, 1.5]),
    }

    weighted_relations = generate_weights_full(relations, distributions)

    print(weighted_relations)
