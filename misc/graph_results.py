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

    plot1 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_1.json'))
    plot2 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_2.json'))
    plot3 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_3.json'))
    plot4 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_4.json'))
    plot5 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_5.json'))
    plot6 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_6.json'))
    plot7 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_7.json'))
    plot8 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_8.json'))
    plot9 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_9.json'))
    plot10 = plt.plot('x', 'y', data = graph_w_ratio('results/core_amount3/core_amount_10.json'))
    plt.legend((plot1[0], plot2[0], plot3[0], plot4[0], plot5[0], plot6[0], plot7[0], plot8[0], plot9[0], plot10[0]), ('1 core', '2 cores', '3 cores', '4 cores', '5 cores', '6 cores', '7 cores', '8 cores', '9 cores', '10 cores'))

    plt.xlabel("Utilization")
    plt.ylabel("Schedulability ratio")
    plt.show()

    f.savefig("core_amounts.pdf", bbox_inches='tight')


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
        y_data.append(sum(success_list[x:x+settings['iterations']]) / settings['iterations'])


    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
        })

    return data_frame

    return plt.plot('x', 'y', data = data_frame)


if __name__ == "__main__":
    main()








