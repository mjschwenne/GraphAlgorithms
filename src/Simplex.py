"""
This program performs the Simplex Algorithm on a linear program given in matrix form.

There are three phases to the simplex algorithm.

- Phase 0: Find a basis solution. This is accomplished using standard linear algebra techniques. First, we row reduce
  the initial tableau given to the program and then use the set of linearly independent rows to find the basis solution
- Phase 1: Find a basis feasible solution. One of the requirements of a linear program in standard form is that the
  value of every variable must be greater than or equal to zero, which is not a requirement in the phase 0 basis
  solution. To do this we introduce an artificial variable with a value of -1 for each negative entry in the solution
  vector. By row reducing or pivoting on the most negative, the smallest value, we can force all of the others to become
  positive. This creates a secondary objective function, which is always feasible. Applying a similar process to phase 2
  we attempt to reduce the value of the secondary objective function to zero. If this is possible then the current
  solution is a basis feasible solution.
- Phase 2: Improve the basis feasible solution. Moving from left to right across the bottom row of the tableau, find
  each negative value and pivot or row reduce an the positive valued entry in that column with the smallest ratio of
  solution entry over tableau entry. Each of these moves will push the solution towards the optimal one. Once all of
  the entries in the final row of the tableau are positive, the optimal solution has been found.

This is a high level overview of the what the algorithm does, to understand why this works, please refer to the
textbook.

NumPy is used only for the ndarray data type and utility functions such as inserting rows and deleting rows.

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
        while tableau[r][c] == 0 and c <= n:
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
            c = -1
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
    # Read in the tableau from the same format as the sample files from my professor for pivot.c
    with open('../linearPrograms/Final-5.txt') as tableau_file:
        if tableau_file.readline() != "begin\n":
            print("Tableau File Error!")
            exit(-1)
        tableau_size = tableau_file.readline().split()
        tableau_size = [int(i) for i in tableau_size]
        tab = np.empty((tableau_size[0], tableau_size[1]))
        for line_index in range(tableau_size[0]):
            line = tableau_file.readline().split()
            line = [float(i) for i in line]
            for entry_index in range(tableau_size[1]):
                tab[line_index][entry_index] = line[entry_index]
    print(f"Read initial tableau as\n{tab}")

    simplex_state, values, solution = simplex(tab)
    if simplex_state is SimplexState.FEASIBLE:
        print(f"The program is FEASIBLE with optimal solution {np.around(values, 2)} yielding z = {round(solution, 2)}")
        print(f"The program is FEASIBLE with optimal solution {values} yielding z = {solution}")
    else:
        print(f"The program is {simplex_state.name}.")
