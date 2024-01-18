import pandas as pd
import numpy as np
import random as rnd

# load ta data and sample solutions
sections_df = pd.read_csv('sections.csv')
tas_df = pd.read_csv('tas.csv')

sol1 = pd.read_csv('test1.csv', header=None).values
sol2 = pd.read_csv('test2.csv', header=None).values
sol3 = pd.read_csv('test3.csv', header=None).values

def overallocation(sol):
    """ Objective Function: Our measure of sortedness for a list of numbers """
    max_assigned = list(tas_df.max_assigned)
    act_assigned = list(sol.sum(axis=1))
    return (
        sum([max(0, act_assigned - max_assigned) for act_assigned, max_assigned in zip(act_assigned, max_assigned)]))


def conflicts(sol):
    """ Objective Function: Reduces number of time conflicts for TAs"""
    times = sections_df.values[:, 2]
    return sum([1 if sum(sol[i]) != len(set([times[j] for j in range(len(times)) if sol[i][j] == 1])) else 0 for i in
                range(len(tas_df.values))])


def undersupport(sol):
    """ Objective Function: minimize total penalty points for sections with fewer TAs than needed """
    ta_needed = sections_df["min_ta"].to_numpy()
    ta_assigned = sol.sum(axis=0)
    return np.sum(np.maximum(0, ta_needed - ta_assigned))


def unwilling(sol):
    """ Objective """
    df_preference = pd.read_csv('tas.csv').iloc[:, 3:]
    times = np.where((df_preference == 'U') & (sol == 1), 1, 0)
    # sum up
    return np.sum(times)


def unpreferred(sol):
    """ Objective function: Minimizes times when tas are assigned to sections marked willing """
    times = np.where((tas_df.values[:, 3:] == 'W') & (sol == 1), 1, 0)
    # sum up
    return np.sum(times)

def random_row_swap(sols, swap=1):
    """ Agent that swaps two random rows in the solution """
    sol = sols[0]
    sol_copy = sol.copy()
    num_rows = len(sol)
    for i in range(swap):
        rand_row0 = rnd.randrange(0, num_rows)
        rand_row1 = rnd.randrange(0, num_rows)
        # print(rand_row0, rand_row1)
        sol_copy[[rand_row0, rand_row1]] = sol_copy[[rand_row1, rand_row0]]
    return sol_copy

def random_flip(sols):
    """ Agent that flips 10 random data points in the solution (0 to 1 or 1 to 0) """
    sol = sols[0]
    rows, cols = sol.shape
    indices = np.random.choice(rows * cols, 10, replace=False)

    sol_flat = sol.ravel()
    sol_flat[indices] = 1 - sol_flat[indices]

    return sol.reshape((rows, cols))

def overallocationHelper(sols):
    ''' Agent that iterates through solution, checks if the TA is overallocated,
    and removes a random section if so '''
    sol = sols[0]
    for i in range(len(sol)):
        if sum(sol[i]) > tas_df.values[i, 2]:
            sol[i, rnd.choice(np.where(sol[i])[0])] = 0
    return sol

def conflictsHelper(sols):
    """ Agent that reduces conflicts by choosing two of every ta's assignments
     and unassigning one if they conflict """
    sol = sols[0]
    times = sections_df.values[:, 2]
    for i in range(len(sol)):
        if sum(sol[i]) >= 2:
            rands = rnd.sample(list(np.where(sol[i])[0]), 2)
            if times[rands[0]] == times[rands[1]]:
                sol[i, rands[0]] = 0
    return sol

def supportHelper(sols):
    """ Agent that reduces undersupport by iterating through sections
    and adding an available ta if section lacks support """
    sol = sols[0]
    min_tas = sections_df.values[:, 6]
    ta_prefs = tas_df.values[:, 3:]
    for i in range(sol.shape[1]):
        if sum(sol[:,i]) < min_tas[i]:
            sol[rnd.choice(np.where((sol[:, i]==0) & (ta_prefs[:, i] != 'U'))[0]), i] = 1
    return sol

def unwilling_fix(sols):
    """ An agent to target the unwilling issue. For 100 iterations:
    randomly picks a section and if they were unwilling,
    make sure they aren't assigned there.
    """
    sol = sols[0]
    sol_copy = sol.copy()
    preferences = pd.read_csv('tas.csv').iloc[:, 3:].values
    num_rows, num_cols = sol_copy.shape
    for i in range(100):
        rand_row = rnd.randrange(0, num_rows)
        rand_col = rnd.randrange(0, num_cols)
        if preferences[rand_row, rand_col] == 'U':
            sol_copy[rand_row, rand_col] = 0
    return sol_copy
