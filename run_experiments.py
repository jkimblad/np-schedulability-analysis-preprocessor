#!/usr/bin/env python3


import subprocess
import random
import json

settings = {
        # Set what ratio of the execution time should be taken by the A-phase and R-phase
        'a_ratio' : 0.1,
        'r_ratio' : 0.1,

        # Amount of tasks in each task set
        'task_amount' : 50,

        # Total utilization of the task set
        'starting_utilization' : 0.1,
        'ending_utilization' : 1.0,
        'utilization_step_size' : 0.1,

        # Physical cores available in the analysis for jobs to be scheduled onto
        'core_amount' : 50,

        # At what window ratio should we start exploring
        # starting_window_ratio : None
        # ending_window_ratio : None
        'window_ratio' : 0.5,

        # How much should we increment the window ratio
        # window_ratio_step_size :  None

        # Task sets per window_ratio_step
        'iterations' : 1,

        # Timeout value for nptest, how long do we allow search for a feasible schedule?
        'timeout' : 5,

        # Seed for random generator
        'seed' : 2
    }


schedulers = ['EDF', 'HU', 'LU', 'LULP', 'LUHP', 'HULP', 'HUHP']

for scheduler in schedulers:


    # Results list
    results = []


    iteration_counter = 0

    # Start experiments
    utilization = settings['starting_utilization']

    # Set random seed
    random.seed(settings['seed'])


    while utilization < settings['ending_utilization']:

        for i in range(settings['iterations']):

            # Generate task-set
            task_output = subprocess.check_output([                                     \
                    "./task_generator.py",                                              \
                    "-o",                                                               \
                    "tasks/task_set_" + str(iteration_counter) + ".csv",                \
                    "-s",                                                               \
                    str(random.randint(1, 1000000)),                                    \
                    "-a",                                                               \
                    str(settings['a_ratio']),                                                       \
                    str(settings['r_ratio']),                                                       \
                    str(settings['task_amount']),                                                   \
                    str(utilization)                                                    \
                    ])
            # print("task: " + task_output.decode())

            # Generate job-set from task-set
            job_output = subprocess.check_output([                                      \
                    "./preprocessor.py",                                                \
                    "-o",                                                               \
                    "jobs/job_set_" + str(iteration_counter) + ".csv",                  \
                    "-w",                                                               \
                    str(settings['window_ratio']),                                                  \
                    "-s",                                                               \
                    scheduler,                                                          \
                    "tasks/task_set_" + str(iteration_counter) + ".csv"                 \
                    ])
            # print("job: " + job_output.decode())

            # Run nptest
            np_result = subprocess.check_output([                                       \
                    "./nptest",                                                         \
                    "-l",                                                               \
                    str(settings['timeout']),                                                       \
                    "-i",                                                               \
                    "AER",                                                              \
                    "-m",                                                               \
                    str(settings['core_amount']),                                                   \
                    "jobs/job_set_" + str(iteration_counter) + ".csv"                   \
                    ])
            # print("np" + np_result.decode())

            # Save results
            temp = {
                'utilization' : utilization,
                'success' : int(np_result.decode().replace(" ", "").split(",")[1])
                }
            results.append(temp)


            iteration_counter += 1

            # Delete created files
            subprocess.run(["rm -rf tasks/* jobs/*"], shell=True)

        # Increase utilization for next loop
        utilization += settings['utilization_step_size']

    output = {
            'settings': settings,
            'results': results
            }

    with open("results/algos/" + scheduler + "_1.json", "w+") as f:
        f.write(json.dumps(output, indent=4))




    
