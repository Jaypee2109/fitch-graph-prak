import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pydot
import math
import random
import copy
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

    print("Percentage deleted        - ", factor * 100)
    print("Special scenario          - ", special)
    print("Empty relations           - ", edgeTuple[0])
    print("Directed relations        - ", edgeTuple["d"])
    print("Bidirected relations      - ", edgeTuple[1])

    return edgeTuple


# count list of list of edges
def count_edges(edgeTuple):
    count = 0

    for key in edgeTuple:
        count += len(edgeTuple[key])

    return count


def generate_di_cograph(nodes):
    nodeId = len(nodes)
    tempNodes = copy.deepcopy(nodes)

    dicotree = nx.DiGraph()

    while len(tempNodes) > 1:
        leftTree = tempNodes.pop(random.randint(0, len(tempNodes) - 1))
        rightTree = tempNodes.pop(random.randint(0, len(tempNodes) - 1))

        if leftTree in nodes:
            dicotree.add_node(leftTree, symbol=leftTree)

        if rightTree in nodes:
            dicotree.add_node(rightTree, symbol=rightTree)

        operation = random.choice(["u", "b", "e"])
        dicotree.add_node(nodeId, symbol=operation)

        dicotree.add_edge(nodeId, leftTree)
        dicotree.add_edge(nodeId, rightTree)

        tempNodes.append(nodeId)

        nodeId += 1

    decoded_dicotree = cotree_to_rel(dicotree)
    dicograph = rel_to_fitch(decoded_dicotree, nodes)

    labels = {node: data["symbol"] for node, data in dicotree.nodes(data=True)}

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

    # Lea
    # nx.draw(dicotree, with_labels=True, labels=labels)
    pos = nx.nx_agraph.graphviz_layout(dicotree, prog="dot")
    nx.draw(dicotree, pos, with_labels=True, labels=labels)

    plt.show()

    return dicograph


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


if __name__ == "__main__":
    path = "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14"

    nodeset_graph = nx.read_graphml(path + "/dFitch.graphml", int).nodes
    edgeTuple = {1: [], "d": [], 0: []}

    # print("bidirect: ", end="")
    edgeTuple[1] = read_pickle(path + "/biRelations.pkl")

    # print("unidirect: ", end="")
    edgeTuple["d"] = read_pickle(path + "/uniRelations.pkl")

    # print("empty: ", end="")
    edgeTuple[0] = read_pickle(path + "/emptyRelations.pkl")

    print()
    print("XENOLOGY GRAPH")
    print("Nodeset                   - ", nodeset_graph)
    print("Empty relations           - ", edgeTuple[0])
    print("Directed relations        - ", edgeTuple["d"])
    print("Bidirected relations      - ", edgeTuple[1])
    print("----------------------------")

    # task 2 & 2b
    partial_graph = reduce_graph(edgeTuple, 0.9)

    # task 3
    nodeset_dicograph = [i for i in range(10)]
    random_dicograph = generate_di_cograph(nodeset_dicograph)
    edgeTuple_dicograph = graph_to_rel(random_dicograph)

    print()
    print("DI-COGRAPH")
    print("Nodeset                   - ", nodeset_dicograph)
    print("Empty relations           - ", edgeTuple_dicograph[0])
    print("Directed relations        - ", edgeTuple_dicograph["d"])
    print("Bidirected relations      - ", edgeTuple_dicograph[1])
    print("----------------------------")

    # task 4
    partial_dicograph = reduce_dicograph(random_dicograph, 0.9)

    # generate weights for partial relations
    weights_graph = create_weights(nodeset_graph, partial_graph, 100)
    weights_dicograph = create_weights(nodeset_dicograph, partial_dicograph, 100)

    # task 5
    # """
    fitch_cotree_graph_012 = algorithm_one(partial_graph, nodeset_graph, (0, 1, 2))
    fitch_cotree_dicograph_012 = algorithm_one(
        partial_dicograph, nodeset_dicograph, (0, 1, 2)
    )
    # """

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
