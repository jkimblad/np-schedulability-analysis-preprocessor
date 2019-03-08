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

    taskSet = Task_Set()
    jobSet = Job_Set()

    # Get user options
    inputArguments = inputParse()

    # Load tasks from input into taskSet
    getTasks(inputArguments.inputFile)

    # Get hyperperiod of task set
    hyperPeriod = taskSet.getHyperPeriod()

    # Generate A and R jobs
    generateJobs()

    
def inputParse():
    parser = argparse.ArgumentParser()

    # Input file
    parser.add_argument("inputFile", help="Input FILE in .csv format", metavar="input")

    # Output file
    parser.add_argument("-o", "--output", dest="outputFile", help="Output FILE", metavar="FILE")

    # How large the A and R windows should be in proportion to each other
    parser.add_argument("-w", "--window", dest="windowSize", help="Determines the ratio between the sizes of A and R windows which within each respective phase can be scheduled as part of the interval from job release to job deadline", metavar="SIZE", type=float, default=0.5)

    return parser.parse_args()

# Return the A and R jobs that a single task would produce within a given hyperperiod as a list of lists
def generateJobs():

    taskSet = Task_Set()
    jobSet = Job_Set()

    hyperPeriod = taskSet.getHyperPeriod()

    # Iterate through all tasks
    for task in taskSet.tasks:
        print(task.task_id)


        # Amount of jobs to be produced
        jobAmount = int(hyperPeriod / task.period)

        for i in range(jobAmount):
            currentTime = i * task.period

            # Create the job ID pair as there are some constraints on how they should be created
            idPair = jobSet.getNextIDPair()
            

            # Create the A job
            aJob = Job()
            aJob.task_id = task.task_id
            aJob.job_id = idPair[0] 
            #Arrival for A is same as arrival for task
            aJob.arrival_min = task.arrival_min
            aJob.arrival_max = task.arrival_max
            aJob.cost_min = task.acquisition
            aJob.cost_max = task.acquisition

            # The deadline of the A job is given by the window ratio given as input
            # TODO
            aJob.deadline = None


            # The priority is given by the tasks priority, but it must have a
            # higher value than all other R-jobs
            #   - Maybe we assign priorities after all jobs have been created allready?


            # Create the R job
            rJob = Job()
            rJob.task_id = task.task_id
            rJob.job_id = idPair[1] 
            #Arrival for A is same as arrival for task
            # TODO
            rJob.arrival_min = None
            rJob.arrival_max = None
            rJob.cost_min = task.restitution
            rJob.cost_max = task.restitution

            # The deadline of the A job is given by the window ratio given as input
            # TODO
            rJob.deadline = None

            # The priority is given by the tasks priority, but it must have a
            # higher value than all other R-jobs
            #   - Maybe we assign priorities after all jobs have been created allready?


            jobSet.addJob(aJob)
            jobSet.addJob(rJob)


# Return the tasks laoded from the input csv as a list of dictionary object
def getTasks(inputFile):
    tasks = []

    task_set = Task_Set()

    # Load in the provided csv file
    with open (inputFile, newline='') as inputFile:
        inputReader = csv.DictReader(inputFile, skipinitialspace=True)
        #Each row represents a task we want to save as an object
        for row in inputReader:
            task = Task()
            #Transform input in each row from string to int
            task.task_id = int(row['id'])
            task.arrival_min = int(row['arrival_min'])
            task.arrival_max = int(row['arrival_max'])
            task.computation_min = int(row['computation_min'])
            task.computation_max = int(row['computation_max'])
            task.acquisition = int(row['acquisition'])
            task.restitution = int(row['restitution'])
            task.deadline = int(row['deadline'])
            task.priority = int(row['priority'])
            task.period = int(row['period'])

            task_set.addTask(task)

class Task:
    
    def __init__(self):
        self.task_id = None
        self.arrival_min = None
        self.arrival_max = None
        self.computation_min = None
        self.computation_max = None
        self.acquisition = None
        self.restitution = None
        self.deadline = None
        self.priority = None
        self.period = None


class Task_Set:

    # Static variables
    tasks = []

    def __init__(self):
        self.current = 0
        self.stop = len(self.tasks)

    # private:
    @staticmethod
    def getHyperPeriod():
        hyperPeriod = 1
        for task in Task_Set.tasks:
            hyperPeriod = Task_Set.__lcm(hyperPeriod, task.period)

        return hyperPeriod
                
    @staticmethod
    def addTask(t):
        Task_Set.tasks.append(t)

    @staticmethod
    def __gcd(a, b):
        # Compute the greatest common divisor of a and b
        while b > 0:
            a, b = b, a % b
        return a

    @staticmethod
    def __lcm(a, b):
        # Compute the lowest common multiple of a and b
        return a * b / Task_Set.__gcd(a, b)


class Job:

    def __init__(self):
        self.task_id = None
        self.job_id = None
        self.arrival_min = None
        self.arrival_max = None
        self.cost_min = None
        self.cost_max = None
        self.deadline = None
        self.priority = None


class Job_Set:

    # Static variables
    jobs = []

    # Print job set as csv
    #TODO
    def printJobs():
        for job in jobs:
            print("")


    @staticmethod
    def addJob(j):
        Job_Set.jobs.append(j)


    def getHighestRestitutionPrio():
        maxPrio = 0;
        for job in jobs:
            if self.__isRestitution(job.job_id):
                maxPrio = max(maxPrio, job.job_id)

        return maxPrio


    def getHighestPrio():
        maxPrio = 0;
        for job in jobs:
            maxPrio = max(maxPrio, job.priority)

        return maxPrio;


    @staticmethod
    def __getHighestID():
        maxID = 0

        for job in Job_Set.jobs:
            maxID = max(maxID, job.job_id)

        return maxID


    def __isRestitution(job_id):
        return job_id % 2


    def getJob(job_id):
        for job in jobs:
            if (job_id == job.job_id):
                return job
        return None;

    # Return next free ID as a pair, one for the next A job and the second for the next R phase
    @staticmethod
    def getNextIDPair():
        highestID = Job_Set.__getHighestID()
        # Check if highest ID is R-phase

        # Highest current Job ID is even
        if(Job_Set.__isRestitution(highestID)):
            return [highestID + 1, highestID + 2]

        # Highest current Job ID is odd
        else:
            return [highestID + 2, highestID + 3]
        






# Run main
if __name__ == '__main__':
    main()

