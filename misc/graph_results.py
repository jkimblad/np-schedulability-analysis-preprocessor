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


    axis_data = graph_w_ratio_averages()
    plot = plt.bar('x', 'y', data = axis_data, width=5)
    plt.xticks(range(10, 100, 10))



    for a,b in zip(axis_data['x'], axis_data['y']):
        plt.text(a, b, str(b))

    plt.ylim(0, 31)
    plt.show()


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
            temp.append(sum(success_list[x:x+settings['iterations']]) * (100 / settings['iterations']))

        temp_sum = 0
        counter = 0
        for value in temp:
            temp_sum += value
            counter +=1

        y_data.append(round(temp_sum / counter, 2))



    
    

    data_frame = pd.DataFrame({
        'x' : x_data,
        'y' : y_data
        })

    return data_frame


if __name__ == "__main__":
    main()








