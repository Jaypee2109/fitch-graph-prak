from lib import *
from wp1 import *
from itertools import product


def generate_weights_alternative(relations, distributions):
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


def scoring_function_average(left, right, relations):
    sum = 0
    cuts = 0

    for edge in relations:
        if (edge[0] in left and edge[1] in right) or (
            edge[1] in left and edge[0] in right
        ):
            sum += relations[edge]
            cuts += 1

    return sum / cuts if cuts > 0 else 0


def scoring_function_sum(left, right, relations):
    sum = 0

    for edge in relations:
        if (edge[0] in left and edge[1] in right) or (
            edge[1] in left and edge[0] in right
        ):
            sum += relations[edge]

    return sum


def generate_weights_set(graph, relations, distributions):
    nodeset = list(graph)
    weighted_relations = {1: {}, 0: {}, "d": {}}

    for type in relations:
        possible_edges = [(u, v) for u, v in product(nodeset, nodeset) if u != v]

        complementary_edges = [
            edge for edge in possible_edges if edge not in relations[type]
        ]

        weighted_existing = generate_weights(
            relations[type],
            distributions["existing"][0],
            distributions["existing"][1],
            distributions["existing"][2],
        )
        weighted_complementary = generate_weights(
            complementary_edges,
            distributions["non_existing"][0],
            distributions["non_existing"][1],
            distributions["non_existing"][2],
        )

        weighted_relations[type] = {**weighted_existing, **weighted_complementary}

    return weighted_relations


def bipartition(graph):
    nodeset = list(graph)

    if len(nodeset) < 2:
        return [nodeset, []]

    random.shuffle(nodeset)

    midpoint = len(nodeset) // 2

    return [nodeset[:midpoint], nodeset[midpoint:]]


if __name__ == "__main__":
    # generate fitch graph based on xenology dataset
    xenology = generate_xenology(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_74"
    )

    relations = xenology["relations"]
    graph = xenology["graph"]

    # define distribution parameters for generating weights alternative
    """
    distributions = {
        1: (random.uniform, [1.0, 1.5]),
        0: (random.random, []),
        "d": (random.uniform, [1.0, 1.5]),
    }
    """

    distributions = {
        "existing": (random.uniform, [1.0, 1.5], True),
        "non_existing": (random.random, [], True),
    }

    weighted_relations = generate_weights_set(graph, relations, distributions)

    fitch_relations_partition = partition_heuristic_scaffold(
        weighted_relations["d"],
        weighted_relations[1],
        weighted_relations[0],
        list(graph.nodes),
        bipartition,
        scoring_function_average,
    )
    print("hier")
    print(sym_diff(relations, fitch_relations_partition, len(graph)))

    """
    fitch_relations_louvain = partition_heuristic_scaffold(
        weighted_relations["d"],
        weighted_relations[1],
        weighted_relations[0],
        list(graph.nodes),
        louvain_custom,
        scoring_function_average,
    )
    """
