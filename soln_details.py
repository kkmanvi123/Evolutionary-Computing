import pandas as pd
import numpy as np

sections_df = pd.read_csv('sections.csv')
tas_df = pd.read_csv('tas.csv')

def write_best_solution(best_solution, best_eval, output_file = 'best_solution.txt'):
    """ Get assigned sections for each TA and assigned TAs for each section. """
    ta_names = tas_df['name'].values
    section_names = sections_df['section'].values

    assigned_sections = {ta_name: [] for ta_name in ta_names}
    assigned_tas = {section_name: [] for section_name in section_names}

    for i, ta_name in enumerate(ta_names):
        for j, section_name in enumerate(section_names):
            if best_solution[i, j] == 1:
                assigned_sections[ta_name].append(section_name)
                assigned_tas[section_name].append(ta_name)

    with open(output_file, 'w') as file:
        file.write("Evaluation Score for Solution:\n")
        file.write(str(best_eval))
        file.write("Assigned TAs for Each Section:\n")
        for section_name, ta_names in assigned_tas.items():
            section_details = sections_df[sections_df['section'] == section_name].iloc[0]
            daytime = section_details['daytime']
            location = section_details['location']
            file.write(f"{str(section_name)} ({daytime}, {location}): {', '.join(map(str, ta_names))}\n")

        file.write("\nBest Solution Array:\n")
        file.write(np.array2string(best_solution, separator=', '))


# test_df = pd.read_csv('test1.csv', header=None)
# test_array = test_df.values