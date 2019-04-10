#!/usr/bin/env python3


import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




def main():

    edf                 = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/EDF_1.json'))
    highUtil            = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/HU_1.json'))
    lowUtil             = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/LU_1.json'))
    lowUtilLowPeriod    = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/LULP_1.json'))
    lowUtilHighPeriod   = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/LUHP_1.json'))
    highUtilLowPeriod   = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/HULP_1.json'))
    highUtilHighPeriod  = plt.plot('x', 'y', data = graph_w_ratio('results/algos_2/HUHP_1.json'))
    plt.legend((edf[0], highUtil[0], lowUtil[0], lowUtilLowPeriod[0], lowUtilHighPeriod[0], highUtilLowPeriod[0], highUtilHighPeriod[0]), ('EDF', 'HU', 'LU', 'LULP', 'LUHP', 'HULP', 'HUHP'))
    plt.show()


def graph_w_ratio(file_name):

    #load data
    with open(file_name) as f:
        data = json.load(f)

    settings = data['settings']
    results = data['results']

    # Create x-axis
    utilization = settings['starting_utilization']
    x_data = []
    while utilization < settings['ending_utilization']:
        x_data.append(utilization)
        utilization += settings['utilization_step_size']

    
    # Create y-axis
    success_list = []
    for result in results:
        success_list.append(result['success'])

    y_data = []
    for x in range (0, len(results), settings['iterations']):
        y_data.append(sum(success_list[x:x+settings['iterations']]) * (100 / settings['iterations']))


    print(len(x_data))
    print(len(y_data))

    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
        })

    return data_frame

    return plt.plot('x', 'y', data = data_frame)


if __name__ == "__main__":
    main()








