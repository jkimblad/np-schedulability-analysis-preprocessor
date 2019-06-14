#!/usr/bin/env python3


import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd







def main():

    # x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # y_data = [0, 0, 0, 0, 0.15, 0.35, 2.05, 2.2, 2.35, 2.4, 2.4, 2.4, 2.4, 2.4]

    # frame = pd.DataFrame({
        # 'x' : x_data,
        # 'y' : y_data
        # })
    # core_plot = plt.plot('x', 'y', data = frame)

    f = plt.figure()


    plot10 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_10.json'))
    plot20 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_20.json'))
    plot30 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_30.json'))
    plot40 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_40.json'))
    plot50 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_50.json'))
    plot60 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_60.json'))
    plot70 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_70.json'))
    plot80 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_80.json'))
    plot90 = plt.plot('x', 'y', data = graph_w_ratio('results/w_ratio3/w_ratio_90.json'))
    plt.legend((plot10[0], plot20[0], plot30[0], plot40[0], plot50[0], plot60[0], plot70[0], plot80[0], plot90[0]), ('10', '20', '30', '40', '50', '60', '70', '80', '90'))
    plt.show()

    plt.xlabel("Utilization")
    plt.ylabel("Average schedulability ratio")

    f.savefig("w_ratio3.pdf", bbox_inches='tight')


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


    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
        })

    return data_frame

    return plt.plot('x', 'y', data = data_frame)


if __name__ == "__main__":
    main()








