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
    edgeTuple = graph_to_rel(dicograph)
    print("VORHER----------------------------", edgeTuple)

    reduce_graph(edgeTuple, factor, special)

    print("NACHHER-------------------------", edgeTuple)

    return edgeTuple


def reduce_graph(edgeTuple, factor, special=False):
    print("original: ", edgeTuple)
    numOfEdges = count_edges(edgeTuple)
    print("number of all edges: ", numOfEdges)

    for key in edgeTuple:
        print(key, " set:")

        edgeList = edgeTuple[key]

        if special and key == "d":
            edgeList.clear()

        else:
            numOfDeletes = math.floor(factor * len(edgeTuple[key]))

            while numOfDeletes > 0:
                deletedElement = edgeList.pop(random.randint(0, len(edgeList) - 1))
                print(deletedElement)
                numOfDeletes -= 1

                symmetricTuple = (deletedElement[1], deletedElement[0])

                if symmetricTuple in edgeList:
                    print("symmetric deleted: ", end="")
                    print(symmetricTuple)
                    edgeList.remove(symmetricTuple)
                    numOfDeletes -= 1

    print("number of all edges: ", count_edges(edgeTuple))
    print("reduced: ", edgeTuple)

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


if __name__ == "__main__":
    edgeTuple = {1: [], "d": [], 0: []}

    # print("bidirect: ", end="")
    edgeTuple[1] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/biRelations.pkl"
    )

    # print("unidirect: ", end="")
    edgeTuple["d"] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/uniRelations.pkl"
    )

    # print("empty: ", end="")
    edgeTuple[0] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/emptyRelations.pkl"
    )

    # task 2 & 2b
    # reduce_graph(edgeTuple, 0.5, False)

    # task 3
    nodes = [i for i in range(5)]
    random_dicograph = generate_di_cograph(nodes)

    # task 4
    reduce_dicograph(random_dicograph, 0.5)
