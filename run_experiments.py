#!/usr/bin/env python3


import subprocess
import random
import json

settings = {
        # Set what ratio of the execution time should be taken by the A-phase and R-phase
        'a_ratio' : 0.1,
        'r_ratio' : 0.1,

        # Amount of tasks in each task set
        'starting_tasks' : 1,
        'ending_tasks' : 100,
        'tasks_step' : 1,

        # Total utilization of the task set
        'utilization' : 0.5,

        # Physical cores available in the analysis for jobs to be scheduled onto
        'core_amount' : 255,

        # At what window ratio should we start exploring
        # starting_window_ratio : None
        # ending_window_ratio : None
        'window_ratio' : 0.6,

        # How much should we increment the window ratio
        # window_ratio_step_size :  None

        # Task sets per tasks_step
        'iterations' : 100,

        # Timeout value for nptest, how long do we allow search for a feasible schedule?
        'timeout' : 5,

        # Seed for random generator
        'seed' : 2
    }

# Results list
results = []


iteration_counter = 0

# Start experiments
tasks = settings['starting_tasks']
utilization = settings['utilization']
window_ratio = settings['window_ratio']

# Set random seed
random.seed(settings['seed'])

while tasks <= settings['ending_tasks']:

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
                str(tasks),                                                   \
                str(utilization)                                                    \
                ])
        # print("task: " + task_output.decode())

        # Generate job-set from task-set
        job_output = subprocess.check_output([                                      \
                "./preprocessor.py",                                                \
                "-o",                                                               \
                "jobs/job_set_" + str(iteration_counter) + ".csv",                  \
                "-w",                                                               \
                str(window_ratio),                                                  \
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
    tasks += settings['tasks_step']

output = {
        'settings': settings,
        'results': results
        }

with open("results/task_amount_1.json", "w+") as f:
    f.write(json.dumps(output, indent=4))





