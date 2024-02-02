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


def query(root):
    for node_filename in os.listdir(root):
        node_filename_path = os.path.join(root, node_filename)

        for configuration_filename in os.listdir(node_filename_path):
            configuration_filename_path = os.path.join(
                node_filename_path, configuration_filename
            )

            for rate_filename in os.listdir(configuration_filename_path):
                rate_filename_path = os.path.join(
                    configuration_filename_path, rate_filename
                )

                configuration = extract_values(configuration_filename)
                rate = re.search(r"(\d+)$", rate_filename)

                # create xenology graph
                xenology = generate_xenology(rate_filename_path)
                xenology_graph = xenology["graph"]
                xenology_relations = xenology["relations"]
                xenology_nodes = xenology["graph"].nodes

                # METADATA
                PFAD = rate_filename_path
                KNOTENZAHL = len(xenology_nodes)
                DUPLIKATION = float(configuration[0])
                VERLUST = float(configuration[1])
                HGT = float(configuration[2])
                EVOLUTIONSRATE = int(rate.group(1))

                distributions = {
                    "existing": (random.uniform, [1.0, 1.5], True),
                    "non_existing": (random.random, [], True),
                }

                median_val = random.choice([True, False])
                reciprocal_val = random.choice([True, False])

                # METADATA
                DISTRIBUTION_EXISTING = "random.uniform"
                DISTRIBUTION_NON_EXISTING = "random.random"
                MEDIAN = median_val
                RECIPROCAL = reciprocal_val

                weighted_relations = generate_weights_set(
                    xenology_graph, xenology_relations, distributions
                )

                # METADATA
                METHOD = "random"

                fitch_relations_random_sum = partition_heuristic_scaffold(
                    weighted_relations["d"],
                    weighted_relations[1],
                    weighted_relations[0],
                    list(xenology_nodes),
                    bipartition,
                    scoring_function_sum,
                    median=median_val,
                    reciprocal=reciprocal_val,
                )

                sym_diff_random_sum = sym_diff(
                    xenology_relations, fitch_relations_random_sum, len(xenology_nodes)
                )

                SCORE = "sum"
                DIFF = sym_diff_random_sum

                append_variables_to_csv(
                    "wp2.csv",
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    DISTRIBUTION_EXISTING=DISTRIBUTION_EXISTING,
                    DISTRIBUTION_NON_EXISTING=DISTRIBUTION_NON_EXISTING,
                    MEDIAN=MEDIAN,
                    RECIPROCAL=RECIPROCAL,
                    METHOD=METHOD,
                    SCORE=SCORE,
                    DIFF=DIFF,
                )

                fitch_relations_random_avg = partition_heuristic_scaffold(
                    weighted_relations["d"],
                    weighted_relations[1],
                    weighted_relations[0],
                    list(xenology_nodes),
                    bipartition,
                    scoring_function_average,
                    median=median_val,
                    reciprocal=reciprocal_val,
                )

                sym_diff_random_avg = sym_diff(
                    xenology_relations, fitch_relations_random_avg, len(xenology_nodes)
                )

                SCORE = "avg"
                DIFF = sym_diff_random_avg

                append_variables_to_csv(
                    "wp2.csv",
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    DISTRIBUTION_EXISTING=DISTRIBUTION_EXISTING,
                    DISTRIBUTION_NON_EXISTING=DISTRIBUTION_NON_EXISTING,
                    MEDIAN=MEDIAN,
                    RECIPROCAL=RECIPROCAL,
                    METHOD=METHOD,
                    SCORE=SCORE,
                    DIFF=DIFF,
                )

                # METADATA
                METHOD = "louvain"

                fitch_relations_louvain_sum = partition_heuristic_scaffold(
                    weighted_relations["d"],
                    weighted_relations[1],
                    weighted_relations[0],
                    list(xenology_nodes),
                    louvain_standard,
                    scoring_function_sum,
                    median=median_val,
                    reciprocal=reciprocal_val,
                )

                sym_diff_louvain_sum = sym_diff(
                    xenology_relations, fitch_relations_louvain_sum, len(xenology_nodes)
                )

                SCORE = "sum"
                DIFF = sym_diff_louvain_sum

                append_variables_to_csv(
                    "wp2.csv",
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    DISTRIBUTION_EXISTING=DISTRIBUTION_EXISTING,
                    DISTRIBUTION_NON_EXISTING=DISTRIBUTION_NON_EXISTING,
                    MEDIAN=MEDIAN,
                    RECIPROCAL=RECIPROCAL,
                    METHOD=METHOD,
                    SCORE=SCORE,
                    DIFF=DIFF,
                )

                fitch_relations_louvain_avg = partition_heuristic_scaffold(
                    weighted_relations["d"],
                    weighted_relations[1],
                    weighted_relations[0],
                    list(xenology_nodes),
                    louvain_standard,
                    scoring_function_average,
                    median=median_val,
                    reciprocal=reciprocal_val,
                )

                sym_diff_louvain_avg = sym_diff(
                    xenology_relations, fitch_relations_louvain_avg, len(xenology_nodes)
                )

                SCORE = "avg"
                DIFF = sym_diff_louvain_avg

                append_variables_to_csv(
                    "wp2.csv",
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    DISTRIBUTION_EXISTING=DISTRIBUTION_EXISTING,
                    DISTRIBUTION_NON_EXISTING=DISTRIBUTION_NON_EXISTING,
                    MEDIAN=MEDIAN,
                    RECIPROCAL=RECIPROCAL,
                    METHOD=METHOD,
                    SCORE=SCORE,
                    DIFF=DIFF,
                )


if __name__ == "__main__":
    query("graph-prak-GFH")
