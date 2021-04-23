"""
This program performs the Simplex Algorithm on a linear program given in matrix form.

NumPy is used only for the ndarray data type

Algorithms 17.2.1, 17.2.2, 17.2.3, 17.2.4 and 17.2.5 on pages 459 - 472
"""

import numpy as np
from enum import Enum


class SimplexState(Enum):
    FEASIBLE = 0
    INFEASIBLE = 1
    UNBOUNDED = 2


def pivot(tableau, row, col):
    """
    In place pivot in the tableau based on entry tableau[row][col]

    Parameters
    ----------
    tableau : np.ndarray
        The tableau or matrix we wish to pivot in
    row : int
        The row of the entry we will pivot on
    col : int
        The column of the entry we will pivot on
    """
    m, n = tableau.shape
    # For each row in the tableau
    for k in range(m):
        # If row k is not the same as the row of the pivoting entry
        if k != row:
            # Iterate over that row and replace it with the reduced version
            scaling_factor = tableau[k][col]
            for h in range(n):
                temp = tableau[k][h] - (scaling_factor / tableau[row][col]) * tableau[row][h]
                tableau[k][h] = temp
        else:
            # If row k is the same row as the pivoting entry, scale the row so that the pivoting entry is one
            scaling_factor = tableau[row][col]
            for h in range(n):
                temp = tableau[row][h] / scaling_factor
                tableau[row][h] = temp


def phase0(tableau):
    """
    Finds a basis solution to the initial tableau

    Parameters
    ----------
    tableau : numpy.ndarray
        The initial tableau of the linear program

    Returns
    -------
    SimplexState
        If we can continue to solve the linear program
    List
        Map of rows to there pivot column
    """
    # Find the bounds for only the adjacency matrix of the linear program but accounting for the extra row and column
    # in the tableau and shifting to index from zero, unlike the textbook
    m, n = tableau.shape
    m -= 2
    n -= 2
    # Store the columns with pivots
    pivots = [-1] * (m + 1)
    # For each row...
    r = 0
    while r <= m:
        c = 0
        # ... find the first columns with a non-zero entry
        while tableau[r][c] == 0:
            c += 1
        if c > n:
            if tableau[r][n + 1] != 0:
                # The linear program is infeasible
                return SimplexState.INFEASIBLE, None
            else:
                # The linear program has rank < m, shift up the rows and delete the row of all zeros
                for i in range(r + 1, m):
                    for j in range(n + 1):
                        tableau[i - 1][j] = tableau[i][j]
                        m -= 1
                        r -= 1
                # This might not work...
                tableau = np.delete(tableau, r, 0)
        else:
            pivot(tableau, r, c)
            pivots[r] = c
        r += 1
    return SimplexState.FEASIBLE, pivots


def phase1(tableau, pivots):
    """
    Performs phase 1 of the simplex algorithm on the tableau, changing the basis solution into a basis feasible one

    Parameters
    ----------
    tableau : numpy.ndarray
        The phase 1 tableau
    pivots : List
        A list of pivots in

    Returns
    -------
    SimplexState
        If the linear program is still feasible or why not
    List
        The list of pivots in each row
    numpy.ndarray
        The new tableau... I'm not happy about returning this but we need to return the local tableau
    """
    # Insert a new column to the left of the adjacency matrix and a row below c transpose
    # New column of all zeros
    tableau = np.insert(tableau, 0, 0, 1)
    # New row of all zeros
    tableau = np.insert(tableau, tableau.shape[0], 0, 0)
    # find the new bounds of the adjacency matrix portion of the tableau
    m, n = tableau.shape
    # There are now two rows under the matrix and an extra -1 to index from zero
    m -= 3
    # Subtract one for the last column, but remember that column 0 is now for the artificial variable
    # Extra -1 to index from zero
    n -= 2
    # Put -1 in the artificial variable if the entry in X_B is negative
    for i in range(m + 1):
        if tableau[i][n + 1] < 0:
            tableau[i][0] = -1
    tableau[m + 2][0] = 1
    # The phase 1 tableau is now complete, find the first pivot
    r = -1
    most_negative = 0
    for i in range(m + 1):
        if tableau[i][n + 1] < most_negative:
            most_negative = tableau[i][n + 1]
            r = i

    # If the basis solution is a basis feasible solution
    if r < 0:
        # Remove the extra row and column from the tableau
        tableau = np.delete(tableau, 0, 1)
        tableau = np.delete(tableau, m + 2, 0)
        return SimplexState.FEASIBLE, pivots, tableau

    # Pivot on the artificial variable for the most negative entry in X_B
    # No need to record it because it will be deleted from the tableau at the end of the phase
    pivot(tableau, r, 0)

    c = 1
    while c <= n:
        if tableau[m + 2][c] < 0:
            # Similar to phase 2, find the positive entry in this column with the smallest ratio to the entries in X_B
            i = 0
            while tableau[i][c] <= 0:
                i += 1
            ratio = tableau[i][n + 1] / tableau[i][c]
            r = i
            i += 1
            while i <= m:
                if tableau[i][c] > 0 and tableau[i][n + 1] / tableau[i][c] < ratio:
                    ratio = tableau[i][n + 1] / tableau[i][c]
                    r = i
                i += 1
            # Pivot on that entry
            pivot(tableau, r, c)
            # Account for the fact that column zero is now the artificial variable and will be removed later
            pivots[r] = c - 1
            c = 1
        c += 1

    # Check to see if the program is still feasible
    # The round() is a lesson learned from ATLAS about very small decimals close to zero
    if round(tableau[m + 2][n + 1], 8) != 0:
        # Remove the extra row and column from the tableau
        tableau = np.delete(tableau, 0, 1)
        tableau = np.delete(tableau, m + 2, 0)
        return SimplexState.INFEASIBLE, None, tableau
    else:
        # Remove the extra row and column from the tableau
        tableau = np.delete(tableau, 0, 1)
        tableau = np.delete(tableau, m + 2, 0)
        return SimplexState.FEASIBLE, pivots, tableau


def phase2(tableau, pivots):
    """
    Performs phase 2 of the simplex algorithm, improving the basis feasible solution, on the given tableau

    Parameters
    ----------
    tableau : numpy.ndarray
        The phase 2 tableau
    pivots : List
        The pivot list returned from phase 1

    Returns
    -------
    SimplexState
        If the linear program is unbounded or still feasible
    List
        Pivots in the complete tableau
    """
    # Find the bounds for only the adjacency matrix of the linear program but accounting for the extra row and column
    # in the tableau and shift to index from 0
    m, n = tableau.shape
    m -= 2
    n -= 2
    c = 0
    while c <= n:
        # Only operate on columns where the value of that variable in the objective function is less than zero
        if tableau[m + 1][c] < 0:
            # Find the first positive entry in column c
            i = 0
            while tableau[i][c] <= 0 and i <= m:
                i += 1
            if i > m:
                return SimplexState.UNBOUNDED, None
            # Ratio of the entry in X_B over A[i][c]
            ratio = tableau[i][n + 1] / tableau[i][c]
            r = i
            i += 1
            # Try to find a better ratio to use
            while i <= m:
                if tableau[i][c] > 0 and tableau[i][n + 1] / tableau[i][c] < ratio:
                    ratio = tableau[i][n + 1] / tableau[i][c]
                    r = i
                i += 1
            pivot(tableau, r, c)
            pivots[r] = c
            c = 1
        c += 1
    return SimplexState.FEASIBLE, pivots


def simplex(tableau):
    """
    Performs the simplex algorithm on the given initial tableau to find the optimal solution

    Parameters
    ----------
    tableau : numpy.ndarray

    Returns
    -------
    SimplexState
        Where the program was feasible, infeasible or unbounded
    List
        Values of each of the variables in the linear program
    float
        The optimal value of the objective function
    """
    # Run phase zero and ensure the linear program is still feasible
    state, pivots = phase0(tableau)
    if state is not SimplexState.FEASIBLE:
        return state, None, None

    # Run phase one and ensure the linear program is still feasible
    state, pivots, tableau = phase1(tableau, pivots)
    if state is not SimplexState.FEASIBLE:
        return state, None, None

    # Run phase two and ensure the linear program is still feasible
    state, pivots = phase2(tableau, pivots)
    if state is not SimplexState.FEASIBLE:
        return state, None, None

    # We found a solution!
    m, n = tableau.shape
    m -= 2
    n -= 2
    x = [0] * (n + 1)
    for i in range(m + 1):
        x[pivots[i]] = tableau[i][n + 1]
    return SimplexState.FEASIBLE, x, -tableau[m + 1][n + 1]


if __name__ == '__main__':
    # tableau in sample1.txt
    # tab = np.array([[1, -3, 1, 0, -6], [1, -1, 0, 1, 0], [-3, 6, 0, 0, 0]], dtype=float)
    # tableau in sample2.txt
    # tab = np.array([[1, 2, 2, 4, 1, 0, 0, 0, -7], [2, -1, -1, 2, 0, 1, 0, 0, 6], [-2, -1, 1, 1, 0, 0, 1, 0, -4],
    #                 [-7, 1, -3, 2, 0, 0, 0, 1, -8], [-1, -1, -1, -1, 0, 0, 0, 0, 0]], dtype=float)
    # tableau in sample3.txt
    # tab = np.array([[1, 2, 3, 4, 1, 0, 0, 10], [-3, 2, -1, 4, 0, 1, 0, -10], [2, 1, 3, 4, 0, 0, 1, 10],
    #                [-2, -3, -1, -4, 0, 0, 0, 0]], dtype=float)
    # tableau in sample4.txt
    # tab = np.array([[1, 2, -1, 4, 1, 0, 0, 10], [-3, 2, 3, 1, 0, 1, 0, -10], [2, -2, -2, 1, 0, 0, 1, 10],
    #                 [-2, -3, 1, -4, 0, 0, 0, 0]], dtype=float)
    # tableau in sample5.txt
    tab = np.array([[-1, 2, 1, 0, 0, 4], [4, 3, 1, 1, 0, 24], [-2, -2, 0, 0, 1, -7], [7, 2, 0, 0, 0, 0]], dtype=float)
    simplex_state, values, solution = simplex(tab)
    if simplex_state is SimplexState.FEASIBLE:
        print(f"The program is FEASIBLE with optimal solution {np.around(values, 2)} yielding z = {round(solution, 2)}")
    else:
        print(f"The program is {simplex_state.name}.")
