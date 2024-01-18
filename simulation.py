from evo import Evo
import ta_sorting as ta
import numpy as np
from collections import defaultdict
import pandas as pd

def main():
    # Creating an instance of the framework
    E = Evo()

    # Register all objectives (fitness criteria)
    E.add_fitness_criteria("overallocation", ta.overallocation)
    E.add_fitness_criteria("conflicts", ta.conflicts)
    E.add_fitness_criteria("undersupport", ta.undersupport)
    E.add_fitness_criteria("unwilling", ta.unwilling)
    E.add_fitness_criteria("unpreferred", ta.unpreferred)

    # Register all the agents
    E.add_agent('swap_row', ta.random_row_swap, 1)
    E.add_agent('random_flips', ta.random_flip, 1)
    E.add_agent('min_unwilling', ta.unwilling_fix, 1)
    E.add_agent('min_overallocation', ta.overallocationHelper, 1)
    E.add_agent('min_conflicts', ta.conflictsHelper, 1)
    E.add_agent('min_undersupport', ta.supportHelper, 1)

    # Initialize the population
    E.add_solution(np.random.randint(2, size=(43, 17), dtype=int))

    # Evolve solutions
    E.evolve(n=100000, dom=100)

    # Build output
    d = defaultdict(list)
    for eval in E.pop.keys():
        for obj in eval:
            d[obj[0]].append(obj[1])

    df = pd.DataFrame(d)
    names = ['swifties']*len(df)
    df.insert(0, 'groupname', names)
    df.to_csv('evo_objectives.csv', index=False)


main()