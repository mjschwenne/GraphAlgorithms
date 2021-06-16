"""
This is Floyd's algorithm for finding the shortest distance between any two pair of vertices in the graph, also
known as the all-paths problem.

It works by using a weighted adjacency matrix such that
    If :math:`u \\rightarrow v` than :math:`A[u, v] = \\text{Wt}(uv)`

    If :math:`u \\not\\rightarrow v` than :math:`A[u, v] = \\infty`

    If :math:`u = v` than :math:`A[u, v] = 0`

It then attempts to route a path from every vertex through every other vertex to the destination vertex.

Algorithm 2.7.1 on page 41
"""

import networkx as nx
import numpy as np


def build_matrix(G):
    """
    Build the weighted adjacency matrix from the graph G.

    If :math:`u \\rightarrow v` than :math:`A[u, v] = \\text{Wt}(uv)`

    If :math:`u \\not\\rightarrow v` than :math:`A[u, v] = \\infty`

    If :math:`u = v` than :math:`A[u, v] = 0`

    Parameters
    ----------
    G : nx.Graph
        The graph that we need to build a weighted adjacency matrix for.

    Returns
    -------
    np.ndarray
        The weighted adjacency matrix
    """
    # Create an n by n matrix of all zeros
    matrix = np.zeros(shape=(len(G), len(G)))
    for v in G:
        for u in G:
            if v == u:
                matrix[v][u] = 0
            elif u in G[v]:
                matrix[v][u] = G[v][u]["weight"]
            else:
                matrix[v][u] = np.inf

    return matrix


def floyd(G):
    """
    Performs Floyd's algorithm for the all-paths problem, returning a matrix such that M[v, u] is the shortest distance
    between `u` and `v`.
    
    Parameters
    ----------
    G : nx.Graph
        The graph we wish to solve the all-paths problem on

    Returns
    -------
    np.ndarray
        An n by n matrix with the shortest distance between any two vertices encoded in it.
    """
    n = len(G)
    matrix = build_matrix(G)
    for k in range(n):
        for v in range(n - 1):
            for w in range(v + 1, n):
                matrix[v][w] = min(matrix[v][w], matrix[v][k] + matrix[k][w])

    return matrix


if __name__ == "__main__":
    graph = nx.readwrite.read_weighted_edgelist(
        "../graphs/weighted_floyd.edgelist", nodetype=int
    )
    print(floyd(graph))
