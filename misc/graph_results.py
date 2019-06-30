#!/usr/bin/env python3


import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




def main():

    f = plt.figure()

    axis_data = graph_algo_averages()
    plot = plt.bar('x', 'y', data = axis_data, width=0.5)

    for a,b in zip(axis_data['x'], axis_data['y']):
        plt.text(x = a, y = b + 0.005, s = str(b), ha='center')


    plt.xlabel("Scheduling algorithm")
    plt.ylabel("Average schedulability ratio")
    plt.ylim(0, 0.3)
    plt.show()

    f.savefig("scheduling_alog_averages.pdf", bbox_inches='tight')


def graph_algo_averages():

    # Create x-axis
    x_data = ["EDF", "HU", "LU", "LULP", "LUHP", "HULP", "HUHP"]


    #Create y-axis
    folder = "algos_8"
    files = [                               \
        'results/' + folder + '/EDF_1.json', \
        'results/' + folder + '/HU_1.json', \
        'results/' + folder + '/LU_1.json', \
        'results/' + folder + '/LULP_1.json', \
        'results/' + folder + '/LUHP_1.json', \
        'results/' + folder + '/HULP_1.json', \
        'results/' + folder + '/HUHP_1.json' \
             ]

    y_data = []

    for result_file in files:

        #load data
        with open(result_file) as f:
            data = json.load(f)

        settings = data['settings']
        results = data['results']

        success_list = []
        for result in results:
            success_list.append(result['success'])

        temp = []
        for x in range (0, len(results), settings['iterations']):
            temp.append(sum(success_list[x:x+settings['iterations']]) / settings['iterations'])

        temp_sum = 0
        counter = 0

        for value in temp:
            temp_sum += value
            counter += 1

        y_data.append(round(temp_sum / counter, 3))


    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
    })

    return data_frame


if __name__ == "__main__":
    main()








