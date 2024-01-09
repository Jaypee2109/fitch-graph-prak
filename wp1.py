import pandas as pd
import math
import random


def read_pickle(filepath):
    listOfEdges = pd.read_pickle(filepath)
    print(listOfEdges)

    return listOfEdges


def reduce_graph(edgeTuple, factor):
    numOfEdges = count_edges(edgeTuple)
    print(numOfEdges)

    for key in edgeTuple:
        numOfDeletes = math.floor(factor * len(edgeTuple[key]))
        edgeList = edgeTuple[key]

        while numOfDeletes > 0:
            deletedElement = edgeList.pop(random.randint(0, len(edgeList) - 1))
            print(deletedElement)

            # TODO remove inverted element :: if...

            numOfDeletes -= 1

    print(numOfDeletes)


# count list of list of edges
def count_edges(edgeTuple):
    count = 0

    for key in edgeTuple:
        count += len(edgeTuple[key])

        print(len(edgeTuple[key]))

    return count


if __name__ == "__main__":
    edgeTuple = {"bidirect": [], "unidirect": [], "empty": []}

    print("bidirect: ", end="")
    edgeTuple["bidirect"] = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/biRelations.pkl"
    )

    print("unidirect: ", end="")
    edgeTuple["unidirect"] = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/uniRelations.pkl"
    )

    print("empty: ", end="")
    edgeTuple["empty"] = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/emptyRelations.pkl"
    )

    reduce_graph(edgeTuple, 0.5)
