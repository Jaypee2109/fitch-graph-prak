import pandas as pd
import math
import random


def read_pickle(filepath):
    listOfEdges = pd.read_pickle(filepath)
    print(listOfEdges)

    return listOfEdges


def reduce_graph(edgeTuple, factor, special=False):
    print("original: ", edgeTuple)
    numOfEdges = count_edges(edgeTuple)
    print("number of all edges: ", numOfEdges)

    for key in edgeTuple:
        print(key + " set:")

        edgeList = edgeTuple[key]

        if special and key == "unidirect":
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


# count list of list of edges
def count_edges(edgeTuple):
    count = 0

    for key in edgeTuple:
        count += len(edgeTuple[key])

    return count


if __name__ == "__main__":
    edgeTuple = {"bidirect": [], "unidirect": [], "empty": []}

    print("bidirect: ", end="")
    edgeTuple["bidirect"] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/biRelations.pkl"
    )

    print("unidirect: ", end="")
    edgeTuple["unidirect"] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/uniRelations.pkl"
    )

    print("empty: ", end="")
    edgeTuple["empty"] = read_pickle(
        "graph-prak-GFH/n25/D0.5_L0.5_H0.25/D0.5_L0.5_H0.25_n25_14/emptyRelations.pkl"
    )

    reduce_graph(edgeTuple, 0.5, True)
