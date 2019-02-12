#!/usr/bin/env python3

# Import libraries
# To read CSV input
import csv
# For LCM
from gmpy2 import lcm
import sys
import argparse

# Constants defining input
EXPECTED_COLUMNS = 8
FILE_INPUT_ARGUMENT = 1
EXPECTED_ARGUMENTS = 2


# Main, execution starts here
def main():

    # Get user options
    inputArguments = inputParse()

    # Get input tasks as a list of dictionaries
    tasks = getTasks()

    #Generate normal jobs
    if not(inputArguments.aerModel):
        # Calculate hyperperiod of task set
        hyperPeriod = 1;
        for task in tasks:
            hyperPeriod = lcm(hyperPeriod, task['period'])

        # Generate each job for each task in the set
        taskJobs = []
        for task in tasks:
            taskJobs.append(generateJobs(task, hyperPeriod))

        # Generate the csv output
        fieldNames = ['Task ID', 'Job ID', 'Arrival min', 'Arrival max', 'Cost min', 'Cost max', 'Deadline', 'Priority']
        writer = csv.DictWriter(inputArguments.outputFile, fieldNames)
        writer.writeheader()
        for task in taskJobs:
            for job in task:
                writer.writerow(job)

    #Generate A and R jobs
    else:

    
def inputParse():
    parser = argparse.ArgumentParser()

    # Input file
    parser.add_argument("inputFile", help="Input FILE in .csv format", metavar="input")

    # Output file
    parser.add_argument("-o", "--output", dest="outputFile", help="Output FILE", metavar="FILE", default=sys.stdout)

    # Create A and R jobs
    parser.add_argument("--aer", action="store_true", dest="aerModel", help="Input is transformed to A and R jobs to be scheduled onto memory")

    return parser.parse_args()


# Return the jobs that a single task would produce within a given hyperperiod as a list of list
def generateJobs(task, hyperPeriod):
    jobs = []
    
    # Amount of jobs to be produced
    jobAmount = int(hyperPeriod / task['period'])

    for i in range(0, jobAmount):
        job = {}
        currentTime = i * task['period']
        job['Task ID'] = task['id']
        job['Job ID'] = 1
        job['Arrival min'] = currentTime + task['arrival_min']
        job['Arrival max'] = currentTime + task['arrival_max']
        job['Cost min'] = task['computation_min']
        job['Cost max'] = task['computation_max']
        job['Deadline'] = currentTime + task['deadline']
        job['Priority'] = task['priority']

        jobs.append(job)

    return jobs


# Return the tasks laoded from the input csv as a list of dictionary object
def getTasks():
    tasks = []
    columns = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "deadline", "priority", "period"]

    # Load in the provided csv file
    with open (sys.argv[FILE_INPUT_ARGUMENT], newline='') as inputFile:
        inputReader = csv.DictReader(inputFile, skipinitialspace=True)
        #Append each input row to dictionary
        for row in inputReader:
            #Transform input in each row from string to int
            for column in columns:
                row[column] = int(row[column])
            tasks.append(row)

    return tasks
                

# Run main
if __name__ == '__main__':
    main()

