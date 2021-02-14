"""
The breadth first search finds the shortest path from a given vertex to
every other vertex in an unweighted simple graph.

A breadth first search uses a queue, a First-In-First-Out (FIFO) data structure, to find the shortest
number of edges needed to make a uv-path from the start vertex u to any other vertex v in the graph.
While there are unprocessed vertices, we pop them off the queue and test to see if we know the distance
they are from vertex u. If that distance is still infinity we add them to the queue and update the distance to
be one father than the current vertex we are processing.

Algorithm 2.4.1 on page 52
"""

import networkx as nx
import math
import queue


def bfs(G, u):
    """
    Perform a breadth first search over G starting at u

    Parameters
    ----------
    G : nx.Graph
        The graph we wish to search
    u : int
        The origin vertex from which the search starts

    Returns
    -------
    List
        A list dist where dist[v] is the distance of the shortest path from u to v.
        Note, dist[u] = 0
    """
    # initialize the distance list to infinity for every vertex except u, which has a distance of 0
    dist = list()
    for v in range(len(G)):
        dist.append(math.inf)
    dist[u] = 0

    # Create a queue and seed vertex u into it.
    # Unlike ScanQ in the textbook, which is just an array we traverse in one direction, this is a proper FIFO queue
    q = queue.Queue()
    q.put(u)
    # So long as there are vertices left to process, get them from the queue
    # and if they do not have a non-infinity distance, update it.
    # Otherwise, we have already found the shortest path to that vertex
    while not q.empty():
        v = q.get()
        for w in G[v]:
            if dist[w] == math.inf:
                q.put(w)
                dist[w] = dist[v] + 1
    return dist


def print_bfs_dist(G, u):
    """
    Perform a breadth first search over G starting with u and print the results.

    Parameters
    ----------
    G : nx.Graph
        The graph we wish to search.
    u : int
        The origin vertex from which the search starts.

    Examples
    --------
    >>> print_bfs_dist(graph, 0)
    Vertex 0: Dist(0, 0) = 0
    Vertex 1: Dist(0, 1) = 1
    Vertex 2: Dist(0, 2) = 1
    Vertex 3: Dist(0, 3) = 1
    Vertex 4: Dist(0, 4) = 2
    Vertex 5: Dist(0, 5) = 2
    Vertex 6: Dist(0, 6) = 2
    Vertex 7: Dist(0, 7) = 2
    Vertex 8: Dist(0, 8) = 2
    Vertex 9: Dist(0, 9) = 2

    Result of a breadth first search on the petersen graph.
    """
    bfs_dist = bfs(G, u)
    for v in range(len(G)):
        print(f"Vertex {v}: Dist({u}, {v}) = {bfs_dist[v]}")


if __name__ == '__main__':
    graph = nx.readwrite.read_adjlist("../graphs/petersen.adjlist", nodetype=int)
    print_bfs_dist(graph, 0)
