import pandas as pd


def read_pickle(filepath):
    listOfEdges = pd.read_pickle(filepath)
    print(listOfEdges)

    return listOfEdges


def reduce_graph(bidirectionalEdges, unidirectionalEdges, emptyEdges, factor):
    print(count_edges([bidirectionalEdges, unidirectionalEdges, emptyEdges]))


def reduce_graph(edgeTuple, factor):
    print(count_edges(edgeTuple))


# count list of list of edges
def count_edges(edgeList):
    count = 0

    for edges in edgeList:
        count += len(edges)

        print(len(edges))

    return count


if __name__ == "__main__":
    print("bidirect: ", end="")
    bidirect = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/biRelations.pkl"
    )

    print("unidirect: ", end="")
    unidirect = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/uniRelations.pkl"
    )

    print("empty: ", end="")
    empty = read_pickle(
        "graph-prak-GFH/n10/D0.3_L0.3_H0.9/D0.3_L0.3_H0.9_n10_12/emptyRelations.pkl"
    )

    reduce_graph(bidirect, unidirect, empty, 0.5)
