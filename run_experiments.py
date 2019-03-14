#!/usr/bin/env python3


import subprocess

# Set what ratio of the execution time should be taken by the A-phase and R-phase
a_ratio = 0.01
r_ratio = 0.01

# Amount of tasks in each task set
task_amount = 10

# Total utilization of the task set
starting_utilization = 0.1
ending_utilization = 10.0
utilization_step_size = 0.1

# Physical cores available in the analysis for jobs to be scheduled onto
core_amount = 100

# At what window ratio should we start exploring
# starting_window_ratio = None
# ending_window_ratio = None
window_ratio = 0.5

# How much should we increment the window ratio
# window_ratio_step_size =  None

# Task sets per window_ratio_step
iterations = 3

# Timeout value for nptest, how long do we allow search for a feasible schedule?
timeout = 5 

# Results list
results = []


iteration_counter = 0

# Start experiments
utilization = starting_utilization

while utilization < ending_utilization:

    for i in range(iterations):

        # Generate task-set
        task_output = subprocess.check_output([                                     \
                "./task_generator.py",                                              \
                "-o",                                                               \
                "tasks/task_set_" + str(iteration_counter) + ".csv",                \
                "-a",                                                               \
                str(a_ratio),                                                       \
                str(r_ratio),                                                       \
                str(task_amount),                                                   \
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
                str(timeout),                                                       \
                "-i",                                                               \
                "AER",                                                              \
                "-m",                                                               \
                str(core_amount),                                                   \
                "jobs/job_set_" + str(iteration_counter) + ".csv"                   \
                ])
        # print("np" + np_result.decode())

        # Save results
        temp = {
            'utilization' : utilization,
            'success' : np_result.decode().replace(" ", "").split(",")[1]
            }
        results.append(temp)
        print("jobset " + str(iteration_counter) + ": " + str(temp))


        iteration_counter += 1

        # Delete created files
        # subprocess.run(["rm -rf task_set.csv job_set.csv"], shell=True)

    # Increase utilization for next loop
    utilization += utilization_step_size

# print (str(results))




    
