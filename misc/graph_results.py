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


    plot10 = plt.plot('x', 'y', data = graph_w_ratio('results/task_amount_4.json'))
    # plt.legend((plot10[0], plot20[0], plot30[0], plot40[0], plot50[0], plot60[0], plot70[0], plot80[0], plot90[0]), ('10', '20', '30', '40', '50', '60', '70', '80', '90'))
    plt.ylabel("schedulable task sets (%)")
    plt.xlabel("Tasks")
    plt.ylim(ymin=0)
    plt.show()


def graph_w_ratio(file_name):

    #load data
    with open(file_name) as f:
        data = json.load(f)

    settings = data['settings']
    results = data['results']

    # Create x-axis
    tasks = settings['starting_tasks']
    x_data = []
    while tasks <= settings['ending_tasks']:
        x_data.append(tasks)
        tasks += settings['tasks_step']

    
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








