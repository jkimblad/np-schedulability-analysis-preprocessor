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
    tasks = readInput(inputArguments)

    # Get hyperperiod of task set
    hyperPeriod = getHyperPeriod(tasks)

    # Generate normal jobs
    if not(inputArguments.aerModel):

        taskJobs = []
        jobId = 0
        # Generate each job for each task in the set
        for task in tasks:
            taskJobs.append(generateJobs(task, hyperPeriod, jobId))
            jobId += len(taskJobs[-1])

        generateOutput(taskJobs, inputArguments.outputFile)

    # Generate A and R jobs
    else:
        taskJobs = []
        jobId = 0
        # Generate each job for each task in the set
        for task in tasks:
            taskJobs.append(generateAerJobs(task, hyperPeriod, jobId))
            jobId += len(taskJobs[-1]) / 2

        generateOutput(taskJobs, inputArguments.outputFile)


# Generate the csv output
def generateOutput(taskJobs, outputName):
    fieldNames = ['Task ID', 'Job ID', 'Arrival min', 'Arrival max', 'Cost min', 'Cost max', 'Deadline', 'Priority']

    outputFile = open(outputName, 'w+') if outputName else sys.stdout
    writer = csv.DictWriter(outputFile, fieldNames)
    writer.writeheader()
    for task in taskJobs:
        for job in task:
            writer.writerow(job)


# Calculate hyperperiod of task set
def getHyperPeriod(tasks):
    hyperPeriod = 1;
    for task in tasks:
        hyperPeriod = lcm(hyperPeriod, task['period'])
    
    return hyperPeriod

    
def inputParse():
    parser = argparse.ArgumentParser()

    # Input file
    parser.add_argument("inputFile", help="Input FILE in .csv format", metavar="input")

    # Output file
    parser.add_argument("-o", "--output", dest="outputFile", help="Output FILE", metavar="FILE")

    # Create A and R jobs
    parser.add_argument("--aer", action="store_true", dest="aerModel", help="Input is transformed to A and R jobs to be scheduled onto memory")

    return parser.parse_args()

# Return the A and R jobs that a single task would produce within a given hyperperiod as a list of lists
def generateAerJobs(task, hyperPeriod, jobId):
    jobs = []

    # Amount of jobs to be produced
    jobAmount = int(hyperPeriod / task['period'])

    for i in range(jobAmount):
        currentTime = i * task['period']

        # Create the A job
        job = {}

        job['Task ID'] = task['id']
        job['Job ID'] = jobId
        job['Arrival min'] = currentTime + task['arrival_min']
        job['Arrival max'] = currentTime + task['arrival_max']
        job['Cost min'] = task['acquisition']
        job['Cost max'] = task['acquisition']
        job['Deadline'] = currentTime + task['deadline'] - (task['computation_max'] + task['restitution'])
        job['Priority'] = task['priority']

        jobs.append(job)


        # Create the R job
        job = {}

        job['Task ID'] = task['id']
        job['Job ID'] = jobId
        job['Arrival min'] = currentTime + task['arrival_min'] + task['acquisition'] + task['computation_min']
        job['Arrival max'] = currentTime + task['arrival_max'] + task['acquisition'] + task['computation_max']
        job['Cost min'] = task['restitution']
        job['Cost max'] = task['restitution']
        job['Deadline'] = currentTime + task['deadline']
        job['Priority'] = task['priority']

        jobs.append(job)

        jobId += 1

    return jobs

# Return the jobs that a single task would produce within a given hyperperiod as a list of lists
def generateJobs(task, hyperPeriod, jobId):
    jobs = []
    
    # Amount of jobs to be produced
    jobAmount = int(hyperPeriod / task['period'])

    for i in range(0, jobAmount):
        job = {}
        currentTime = i * task['period']
        job['Task ID'] = task['id']
        job['Job ID'] = jobId
        job['Arrival min'] = currentTime + task['arrival_min']
        job['Arrival max'] = currentTime + task['arrival_max']
        job['Cost min'] = task['computation_min']
        job['Cost max'] = task['computation_max']
        job['Deadline'] = currentTime + task['deadline']
        job['Priority'] = task['priority']

        jobs.append(job)

        jobId += 1

    return jobs

def readInput(inputArguments):
    #Check if input contains A and R times as well
    if (inputArguments.aerModel):
        columns = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "acquisition", "restitution", "deadline", "priority", "period"]
        return getTasks(columns, inputArguments)

    else:
        columns = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "deadline", "priority", "period"]
        return getTasks(columns, inputArguments)


# Return the tasks laoded from the input csv as a list of dictionary object
def getTasks(columns, inputArguments):
    tasks = []

    # Load in the provided csv file
    with open (inputArguments.inputFile, newline='') as inputFile:
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

