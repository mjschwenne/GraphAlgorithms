"""
This algorithm takes a list of degree sequence and determines if it is graphic.
If it is graphic, we will generate a graph with that degree sequence.

Starting at the vertex with highest degree, connect it to that many vertices of the next highest degree.
Then decrease the remaining degree of those vertices by moving them from one list to the next lowest list.
If there are no vertices which can still accept the edge, then we know that the sequence is not graphic.

Algorithm 1.2.1 on page 12
"""

import networkx as nx
import matplotlib.pyplot as plt


def graphic(deg_seq):
    """
    Tests the seq to see if it is graphic.

    Parameters
    ----------
    deg_seq : List of int
        The sequence of degree for a proposed graph, in any order.

    Returns
    -------
    nx.Graph
        A graph with a degree sequence `deg_seq` or None if the sequence is not graphic.
    """
    # We assume that the degree sequence is true so that we can use this as a control variable in our loops
    is_graphic = True

    # Create the graph object
    G = nx.Graph()

    # Create the list of lists to track the outstanding degrees.
    pts = list()
    for x in deg_seq:
        pts.append(list())

    # Create a temporary list to store vertices between degree updates
    temp = list()
    for x in deg_seq:
        temp.append(list())

    # Sort the degree sequence
    deg_seq.sort(reverse=True)

    # Insert the degrees into the Pts list of lists.
    # Also add the vertex to the Graph.
    for x in range(len(deg_seq)):
        if deg_seq[x] >= len(deg_seq):
            is_graphic = False
        else:
            pts[deg_seq[x]].append(x)
            # We add one to shift from Python's zero indexing to start at vertex 1
            G.add_node(x + 1)

    # Loop over all the possible vertex degrees starting with the largest
    for k in reversed(range(len(deg_seq))):
        while len(pts[k]) > 0 and is_graphic:
            u = pts[k][0]
            pts[k].pop(0)
            # Join u to the next k vertices of largest degree
            i = k
            for j in range(1, k + 1):
                while len(pts[i]) == 0:
                    i = i - 1
                    if i == 0:
                        is_graphic = False
                v = pts[i][0]
                pts[i].pop(0)
                # We add one to shift from Python's zero indexing to one indexing
                G.add_edge(u + 1, v + 1)
                temp[i].append(v)
            # Transfer the vertices down in degree
            for j in reversed(range(k + 1)):
                while len(temp[j]) > 0:
                    v = temp[j][0]
                    temp[j].pop(0)
                    pts[j - 1].append(v)

    if is_graphic:
        return G
    else:
        return None


def print_is_graphic(deg_seq):
    """
    Takes the degree sequence, tests if it is graphic and then prints the result.

    Parameters
    ----------
    deg_seq : List of int
        The degree sequence to be tested, in any order.

    Examples
    --------
    >>> print_is_graphic([4, 4, 4, 4, 4])
    The degree sequence is graphic!

    This is the degree sequence for the complete graph on 5 vertices.

    >>> print_is_graphic([7, 6, 6, 6, 5, 5, 2, 1])
    This sequence is not graphic!

    This sequence is not graphic becuase there are too many vertices of degree 6.
    """
    graph = graphic(deg_seq)
    if graph is not None:
        print("The degree sequence is graphic!")
    else:
        print("This sequence is not graphic!")


def display_graphic_seq(deg_seq):
    """
    Take the degree sequence, tests if it is graphic and then displays the result.

    Parameters
    ----------
    deg_seq : List of int
        The degree sequence to be tested.
    """
    graph = graphic(deg_seq)
    if graph is not None:
        nx.draw_circular(
            graph, with_labels=True, font_weight="bold", font_color="white"
        )
        plt.show()


if __name__ == "__main__":
    print_is_graphic([7, 6, 6, 6, 5, 5, 2, 1])
