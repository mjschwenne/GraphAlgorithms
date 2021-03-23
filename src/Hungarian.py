"""
The Hungarian algorithm for finding the maximum matching in a bipartite graph. We use a breadth first search to find


Algorithm 9.2.1 on page 174
"""
import networkx as nx


def augment(match, prev_pt, y):
    """
    Take the augmenting path encoded in `prev_pt` and `match` and flip it so we increase the number of edges in the
    matching by one.

    Parameters
    ----------
    match : dict
        The current matching
    prev_pt : dict
        The BFS path that houses an augmenting path
    y : int
        The ending point on the path
    """
    # flip all of the edges on the augmenting path
    while y is not None:
        w = prev_pt[y]
        match[y] = w
        v = match[w]
        match[w] = y
        y = v


def hungarian(G, X):
    """
    Performs the hungarian algorithm to find a maximal matching in the bipartite graph

    Parameters
    ----------
    G : nx.Graph
        A bipartite graph to find the matching in
    X : set
        One of the partitions in the bipartite graph

    Returns
    -------
    dict
        A dictionary so that each vertex is related to its matched vertex
    """
    # This is a destructive algorithm, so we will copy the graph into a new one
    h = G.copy()
    # Recorde which vertex is matching to another
    match = {}
    for v in h:
        match[v] = None
    # Loop over the vertices in the give partition
    for v in X:
        # u is unsaturated
        # While described in the text as a 'queue', s is not one. We need the vertices to accumulate in s so that they
        # can be deleted later
        print(match)
        s = [v]
        ns = set()
        prev_pt = {}
        k = 0
        next_vert = False
        while not next_vert and k < len(s):
            x = s[k]
            print(f"x: {x}, s: {s}, h[{x}] = {h[x]}")
            for y in h[x]:
                print(f"y: {y}, match[{y}] = {match[y]}")
                if y not in ns:
                    ns.add(y)
                    prev_pt[y] = x
                    if match[y] is None:
                        # Augmenting path found
                        augment(match, prev_pt, y)
                        next_vert = True
                        break
                    s.append(match[y])
            k += 1
        if not next_vert:
            print(f"remove {s} and {ns}")
            h.remove_nodes_from(s)
            h.remove_nodes_from(ns)
    # the match dictionary now has the completed matching, we can return it
    return match


if __name__ == '__main__':
    graph = nx.readwrite.read_adjlist("../graphs/bipartite.adjlist", nodetype=int)
    print(hungarian(graph, {0, 1, 2, 3}))
