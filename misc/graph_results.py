#!/usr/bin/env python3


import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd







def main():

    f = plt.figure()
    axis_data = graph_w_ratio_averages()
    plot = plt.bar('x', 'y', data = axis_data, width=5)
    plt.xticks(range(10, 100, 10))



    for a,b in zip(axis_data['x'], axis_data['y']):
        plt.text(x = a - 4, y = b + 0.005, s = str(b))

    plt.xlabel("Window ratio(%)")
    plt.ylabel("Average schedulability ratio")
    plt.ylim(0, 0.3)
    plt.show()

    f.savefig("window_ratio.pdf", bbox_inches='tight')


def graph_w_ratio_averages():

    # Create x-axis
    x_data = range(10, 100, 10)

    # Create y-axis
    files = ['results/w_ratio2/w_ratio_10.json', 'results/w_ratio2/w_ratio_20.json', 'results/w_ratio2/w_ratio_30.json', 'results/w_ratio2/w_ratio_40.json', 'results/w_ratio2/w_ratio_50.json', 'results/w_ratio2/w_ratio_60.json', 'results/w_ratio2/w_ratio_70.json', 'results/w_ratio2/w_ratio_80.json', 'results/w_ratio2/w_ratio_90.json']


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
            counter +=1

        y_data.append(round(temp_sum / counter, 3))



    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
        })

    return data_frame


if __name__ == "__main__":
    main()








