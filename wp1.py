import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pydot
import math
import random
import copy
import os
import re
import csv
from lib import *


def read_pickle(filepath):
    listOfEdges = pd.read_pickle(filepath)
    # print(listOfEdges)

    return listOfEdges


def reduce_dicograph(dicograph, factor, special=False):
    edgeTuple_dicograph = graph_to_rel(dicograph)

    reduce_graph(edgeTuple_dicograph, factor, special)

    return edgeTuple_dicograph


def reduce_graph(edgeTuple, factor, special=False):
    for key in edgeTuple:
        edgeList = edgeTuple[key]

        if special and key == "d":
            edgeList.clear()

        else:
            numOfDeletes = math.floor(factor * len(edgeTuple[key]))

            while numOfDeletes > 0:
                deletedElement = edgeList.pop(random.randint(0, len(edgeList) - 1))
                numOfDeletes -= 1

                symmetricTuple = (deletedElement[1], deletedElement[0])

                if symmetricTuple in edgeList:
                    edgeList.remove(symmetricTuple)
                    numOfDeletes -= 1

    return edgeTuple


# count list of list of edges
def count_edges(edgeTuple):
    count = 0

    for key in edgeTuple:
        count += len(edgeTuple[key])

    return count


def generate_xenology(path):
    graph = nx.read_graphml(path + "/dFitch.graphml", node_type=int)
    # relations = {1: [], "d": [], 0: []}
    # relations[1] = read_pickle(path + "/biRelations.pkl")
    # relations["d"] = read_pickle(path + "/uniRelations.pkl")
    # relations[0] = read_pickle(path + "/emptyRelations.pkl")

    relations = graph_to_rel(graph)

    return {"graph": graph, "relations": relations}


def generate_di_cograph(nodeset):
    nodeId = len(nodeset)
    tempNodes = copy.deepcopy(nodeset)

    dicotree = nx.DiGraph()

    while len(tempNodes) > 1:
        leftTree = tempNodes.pop(random.randint(0, len(tempNodes) - 1))
        rightTree = tempNodes.pop(random.randint(0, len(tempNodes) - 1))

        if leftTree in nodeset:
            dicotree.add_node(leftTree, symbol=leftTree)

        if rightTree in nodeset:
            dicotree.add_node(rightTree, symbol=rightTree)

        operation = random.choice(["u", "b", "e"])
        dicotree.add_node(nodeId, symbol=operation)

        dicotree.add_edge(nodeId, leftTree)
        dicotree.add_edge(nodeId, rightTree)

        tempNodes.append(nodeId)

        nodeId += 1

    # reverse the nodes of the dicotree
    reversed_dicotree = type(dicotree)()

    reversed_nodelist = list(reversed(list(dicotree.nodes(data=True))))
    reversed_dicotree.add_nodes_from(reversed_nodelist)

    reversed_dicotree.add_edges_from(dicotree.edges())

    labels = {node: data["symbol"] for node, data in reversed_dicotree.nodes(data=True)}
    pos = nx.nx_agraph.graphviz_layout(reversed_dicotree, prog="dot")
    nx.draw(reversed_dicotree, pos, with_labels=True, labels=labels)

    # plt.show()

    decoded_dicotree = cotree_to_rel(reversed_dicotree)
    dicograph = rel_to_fitch(decoded_dicotree, nodeset)

    """"
    for edge in list(dicotree.edges):
        node1, node2 = edge
        label1 = dicotree.nodes[node1].get("label", None)
        label2 = dicotree.nodes[node2].get("label", None)

        # Check if both nodes have labels and the labels match
        if label1 is not None and label2 is not None and label1 == label2:
            # Contract the edge
            graph = nx.contracted_edge(graph, edge)
    """

    return {"graph": dicograph, "relations": decoded_dicotree}


def create_weights(nodes, relations, edge_value, non_edge_value=0):
    weights = {"uni_weighted": {}, "bi_weighted": {}, "empty_weighted": {}}

    for node in nodes:
        for pairNode in nodes:
            if node == pairNode:
                continue

            relationTuple = (node, pairNode)

            if relationTuple in relations[0]:
                weights["empty_weighted"][relationTuple] = edge_value
            else:
                weights["empty_weighted"][relationTuple] = non_edge_value

            if relationTuple in relations[1]:
                weights["bi_weighted"][relationTuple] = edge_value
            else:
                weights["bi_weighted"][relationTuple] = non_edge_value

            if relationTuple in relations["d"]:
                weights["uni_weighted"][relationTuple] = edge_value
            else:
                weights["uni_weighted"][relationTuple] = non_edge_value

    return weights


def benchmark_dicograph(graph, deletionRate, order):
    nodeset = graph.nodes
    relations = graph_to_rel(graph)
    partial_dicograph = reduce_dicograph(graph, deletionRate)

    try:
        fitch_cotree_dicograph = algorithm_one(partial_dicograph, nodeset, order)
        symDiffAlgorithmOne = sym_diff(
            relations, cotree_to_rel(fitch_cotree_dicograph), len(nodeset)
        )

        weights_dicograph = create_weights(nodeset, partial_dicograph, 100)

        fitch_relations_dicograph__greedy = algorithm_two(
            nodeset,
            weights_dicograph["uni_weighted"],
            weights_dicograph["bi_weighted"],
            weights_dicograph["empty_weighted"],
        )

        symDiffAlgorithmTwo = sym_diff(
            relations, fitch_relations_dicograph__greedy, len(nodeset)
        )

        print("----------------------------")
        print("1: Completed E*           - ", fitch_cotree_dicograph)
        print("1: Symmetric difference   - ", symDiffAlgorithmOne)
        print("2: Greedy Completed E*    - ", fitch_relations_dicograph__greedy)
        print("2: Symmetric difference   - ", symDiffAlgorithmTwo)

        isFitch = True

    except:
        isFitch = False

    print("Is reduced graph fitch?   - ", isFitch)

    return 1 if isFitch else 0


def benchmark_xenology(nodeset, relations, deletionRate, order):
    partial_graph = reduce_graph(relations, deletionRate)

    fitch_cotree_graph = algorithm_one(partial_graph, nodeset, order)
    symDiffAlgorithmOne = sym_diff(
        relations, cotree_to_rel(fitch_cotree_graph), len(nodeset)
    )

    weights_graph = create_weights(nodeset, partial_graph, 100)

    fitch_relations_graph_greedy = algorithm_two(
        nodeset,
        weights_graph["uni_weighted"],
        weights_graph["bi_weighted"],
        weights_graph["empty_weighted"],
    )
    symDiffAlgorithmTwo = sym_diff(
        relations, fitch_relations_graph_greedy, len(nodeset)
    )

    print("----------------------------")
    print("1: Completed E*           - ", fitch_cotree_graph)
    print("1: Symmetric difference   - ", symDiffAlgorithmOne)
    print("2: Greedy Completed E*    - ", fitch_relations_graph_greedy)
    print("2: Symmetric difference   - ", symDiffAlgorithmTwo)


def extract_values(input_string):
    """
    Extrahiert die Zahlen aus einem String im Format Dx.x_Lx.x_Hx.x.

    Parameters:
    - input_string (str): Der Eingangsstring.

    Returns:
    - tuple: Ein Tupel mit den extrahierten Werten (D-Wert, L-Wert, H-Wert).
    """
    pattern = r"D(\d+\.\d+)_L(\d+\.\d+)_H(\d+\.\d+)"
    match = re.match(pattern, input_string)

    if match:
        d_value = float(match.group(1))
        l_value = float(match.group(2))
        h_value = float(match.group(3))
        return d_value, l_value, h_value
    else:
        return None


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
                xenology_relations = xenology["relations"]
                xenology_nodes = xenology["graph"].nodes

                # METADATA
                TYP = "XENOLOGY"
                PFAD = rate_filename_path
                KNOTENZAHL = len(xenology_nodes)
                DUPLIKATION = float(configuration[0])
                VERLUST = float(configuration[1])
                HGT = float(configuration[2])
                EVOLUTIONSRATE = int(rate.group(1))

                # METADATA
                BI_ANZAHL = len(xenology_relations[1])
                DI_ANZAHL = len(xenology_relations["d"])
                EM_ANZAHL = len(xenology_relations[0])
                FITCH = True

                deletion_rate_percentage = round(random.uniform(0.1, 0.9), 1)
                special_scenario = random.choice([True, False])
                xenology_partial = reduce_graph(
                    xenology_relations, deletion_rate_percentage, special_scenario
                )

                # METADATA
                DELETION_RATE = deletion_rate_percentage
                SPECIAL = special_scenario
                PARTIAL_BI_ANZAHL = len(xenology_partial[1])
                PARTIAL_DI_ANZAHL = len(xenology_partial["d"])
                PARTIAL_EM_ANZAHL = len(xenology_partial[0])

                isFitch = False
                symDiffAlgorithmOne = -1.0
                symDiffAlgorithmTwo = -1.0
                nums = [0, 1, 2]
                random.shuffle(nums)
                order = tuple(nums)

                try:
                    fitch_cotree_graph = algorithm_one(
                        xenology_partial, xenology_nodes, order
                    )
                    symDiffAlgorithmOne = sym_diff(
                        xenology_relations,
                        cotree_to_rel(fitch_cotree_graph),
                        len(xenology_nodes),
                    )

                    isFitch = True

                    weights_graph = create_weights(
                        xenology_nodes, xenology_partial, 100
                    )

                    fitch_relations_graph_greedy = algorithm_two(
                        xenology_nodes,
                        weights_graph["uni_weighted"],
                        weights_graph["bi_weighted"],
                        weights_graph["empty_weighted"],
                    )
                    symDiffAlgorithmTwo = sym_diff(
                        xenology_relations,
                        fitch_relations_graph_greedy,
                        len(xenology_nodes),
                    )
                except:
                    isFitch = False
                    # print("NO FITCH XENOLOGY")

                PARTIAL_FITCH = isFitch
                ALGO_ONE_ORDER = order
                ALGO_ONE_DIFF = symDiffAlgorithmOne
                ALGO_TWO_DIFF = symDiffAlgorithmTwo

                append_variables_to_csv(
                    "wp1.csv",
                    TYP=TYP,
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    BI_ANZAHL=BI_ANZAHL,
                    DI_ANZAHL=DI_ANZAHL,
                    EM_ANZAHL=EM_ANZAHL,
                    FITCH=FITCH,
                    DELETION_RATE=DELETION_RATE,
                    SPECIAL=SPECIAL,
                    PARTIAL_BI_ANZAHL=PARTIAL_BI_ANZAHL,
                    PARTIAL_DI_ANZAHL=PARTIAL_DI_ANZAHL,
                    PARTIAL_EM_ANZAHL=PARTIAL_EM_ANZAHL,
                    PARTIAL_FITCH=PARTIAL_FITCH,
                    ALGO_ONE_ORDER=ALGO_ONE_ORDER,
                    ALGO_ONE_DIFF=ALGO_ONE_DIFF,
                    ALGO_TWO_DIFF=ALGO_TWO_DIFF,
                )

                # ---------------------------------------
                # RANDOM DICOGRAPH

                dicograph_wrapper = generate_di_cograph(list(xenology_nodes))
                dicograph = dicograph_wrapper["graph"]
                dicograph_relations = dicograph_wrapper["relations"]
                dicograph_nodes = list(xenology_nodes)

                # METADATA
                TYP = "DI_COGRAPH"
                PFAD = ""
                KNOTENZAHL = len(dicograph_nodes)
                DUPLIKATION = -1.0
                VERLUST = -1.0
                HGT = -1.0
                EVOLUTIONSRATE = -1

                # METADATA
                BI_ANZAHL = len(dicograph_relations[1])
                DI_ANZAHL = len(dicograph_relations["d"])
                EM_ANZAHL = len(dicograph_relations[0])
                FITCH = check_fitch_graph(dicograph)

                partial_dicograph = reduce_dicograph(
                    dicograph, deletion_rate_percentage, special_scenario
                )

                # METADATA
                DELETION_RATE = deletion_rate_percentage
                SPECIAL = special_scenario
                PARTIAL_BI_ANZAHL = len(partial_dicograph[1])
                PARTIAL_DI_ANZAHL = len(partial_dicograph["d"])
                PARTIAL_EM_ANZAHL = len(partial_dicograph[0])

                isFitch = False
                symDiffAlgorithmOne = -1.0
                symDiffAlgorithmTwo = -1.0

                try:
                    fitch_cotree_dicograph = algorithm_one(
                        partial_dicograph, dicograph_nodes, order
                    )
                    symDiffAlgorithmOne = sym_diff(
                        dicograph_relations,
                        cotree_to_rel(fitch_cotree_dicograph),
                        len(dicograph_nodes),
                    )

                    isFitch = True

                    weights_dicograph = create_weights(
                        dicograph_nodes, partial_dicograph, 100
                    )

                    fitch_relations_dicograph_greedy = algorithm_two(
                        dicograph_nodes,
                        weights_dicograph["uni_weighted"],
                        weights_dicograph["bi_weighted"],
                        weights_dicograph["empty_weighted"],
                    )
                    symDiffAlgorithmTwo = sym_diff(
                        dicograph_relations,
                        fitch_relations_dicograph_greedy,
                        len(dicograph_nodes),
                    )
                except:
                    isFitch = False
                    # print("NO FITCH XENOLOGY")

                PARTIAL_FITCH = isFitch
                ALGO_ONE_ORDER = order
                ALGO_ONE_DIFF = symDiffAlgorithmOne
                ALGO_TWO_DIFF = symDiffAlgorithmTwo

                append_variables_to_csv(
                    "wp1.csv",
                    TYP=TYP,
                    PFAD=PFAD,
                    KNOTENZAHL=KNOTENZAHL,
                    DUPLIKATION=DUPLIKATION,
                    VERLUST=VERLUST,
                    HGT=HGT,
                    EVOLUTIONSRATE=EVOLUTIONSRATE,
                    BI_ANZAHL=BI_ANZAHL,
                    DI_ANZAHL=DI_ANZAHL,
                    EM_ANZAHL=EM_ANZAHL,
                    FITCH=FITCH,
                    DELETION_RATE=DELETION_RATE,
                    SPECIAL=SPECIAL,
                    PARTIAL_BI_ANZAHL=PARTIAL_BI_ANZAHL,
                    PARTIAL_DI_ANZAHL=PARTIAL_DI_ANZAHL,
                    PARTIAL_EM_ANZAHL=PARTIAL_EM_ANZAHL,
                    PARTIAL_FITCH=PARTIAL_FITCH,
                    ALGO_ONE_ORDER=ALGO_ONE_ORDER,
                    ALGO_ONE_DIFF=ALGO_ONE_DIFF,
                    ALGO_TWO_DIFF=ALGO_TWO_DIFF,
                )


def append_variables_to_csv(file_name, **kwargs):
    """
    Fügt eine neue Zeile mit den Werten der Variablen zur CSV-Datei hinzu.

    Parameters:
    - file_name (str): Der Dateiname der CSV-Datei.
    - **kwargs: Variablen und ihre Werte.
    """
    file_path = os.path.join(os.getcwd() + "/csv", file_name)
    all_columns = list(kwargs.keys())

    # Überprüfe, ob die Datei leer ist
    is_empty = not os.path.isfile(file_path) or os.stat(file_path).st_size == 0

    with open(file_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_columns)

        # Schreibe die Überschriften nur, wenn die Datei leer ist
        if is_empty:
            writer.writeheader()

        row_data = {column: kwargs.get(column, "") for column in all_columns}
        writer.writerow(row_data)


if __name__ == "__main__":
    query("graph-prak-GFH")
    TYP = ""
    PFAD = ""
    KNOTENZAHL = -1
    DUPLIKATION = -1.0
    VERLUST = -1.0
    HGT = -1.0
    EVOLUTIONSRATE = -1
    BI_ANZAHL = -1
    DI_ANZAHL = -1
    EM_ANZAHL = -1
    FITCH = False
    DELETION_RATE = -1.0
    SPECIAL = False
    PARTIAL_BI_ANZAHL = -1
    PARTIAL_DI_ANZAHL = -1
    PARTIAL_EM_ANZAHL = -1
    PARTIAL_FITCH = False
    ALGO_ONE_ORDER = (-1, -1, -1)
    ALGO_ONE_DIFF = -1.0
    ALGO_TWO_DIFF = -1.0

    """
    # task 5 create partial tuples on dicograph
    partial_dicograph = reduce_dicograph(random_dicograph, 0.9)

    # task 6
    fitch_cotree_graph_012 = algorithm_one(partial_graph, nodeset_graph, (0, 1, 2))
    fitch_cotree_dicograph_012 = algorithm_one(
        partial_dicograph, nodeset_dicograph, (0, 1, 2)
    )

    # generate weights for partial relations
    weights_graph = create_weights(nodeset_graph, partial_graph, 100)
    weights_dicograph = create_weights(nodeset_dicograph, partial_dicograph, 100)

    fitch_relations_graph_greedy = algorithm_two(
        nodeset_graph,
        weights_graph["uni_weighted"],
        weights_graph["bi_weighted"],
        weights_graph["empty_weighted"],
    )
    fitch_relations_dicograph__greedy = algorithm_two(
        nodeset_dicograph,
        weights_dicograph["uni_weighted"],
        weights_dicograph["bi_weighted"],
        weights_dicograph["empty_weighted"],
    )

    print("Completed E*              - ", fitch_cotree_graph_012)
    print("Completed E*              - ", fitch_cotree_dicograph_012)
    print("Greedy Completed E*       - ", fitch_relations_graph_greedy)
    print("Greedy Completed E*       - ", fitch_relations_dicograph__greedy)
    """
