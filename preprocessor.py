#!/usr/bin/env python3

# Import libraries
# To read CSV input
import csv
import sys
import argparse
# For ceiling function
from math import ceil

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

    scheduler = inputArguments.scheduler
    windowSize = inputArguments.windowSize

    # Load tasks from input into taskSet
    getTasks(inputArguments.inputFile)

    # Get hyperperiod of task set
    hyperPeriod = taskSet.getHyperPeriod()

    # Generate A and R jobs
    generateJobs(windowSize)

    # Priorities must be assigned after all jobs have been created
    assignJobPriorities(scheduler)

    jobSet.printJobs(inputArguments.outputFile)

    
def inputParse():
    parser = argparse.ArgumentParser()

    # Input file
    parser.add_argument("inputFile", help="Input FILE in .csv format", metavar="input")

    # Output file
    parser.add_argument("-o", "--output", dest="outputFile", help="Output FILE", metavar="FILE")

    # How large the A and R windows should be in proportion to each other
    parser.add_argument("-w", "--window", dest="windowSize", help="Determines the ratio between the sizes of A and R windows which within each respective phase can be scheduled as part of the interval from job release to job deadline", metavar="SIZE", type=float, default=0.5)

    # Scheduling algorithm used
    parser.add_argument("-s", "--scheduler", dest="scheduler", help="What scheduling algorithm to be used", choices=['EDF', 'HU', 'LU', 'LULP', 'LUHP', 'HULP', 'HUHP'])

    return parser.parse_args()


def assignJobPriorities(scheduler):

    taskSet = Task_Set()
    jobSet = Job_Set()


    # low util is high prio
    if(scheduler == 'LU'):
        lowUtilPriorities(jobSet, taskSet)

    # high util is high prio
    elif(scheduler == 'HU'):
        highUtilPriorities(jobSet, taskSet)

    # Task-level:
        # Lowest utility highest prio
    # Period-level:
        # Lowest period highest prio
    elif(scheduler == 'LULP'):
        lowUtilLowPeriodPriorities(jobSet, taskSet)

    # Task-level:
        # Lowest utility highest prio
    # Period-level:
        # Highest period highest prio
    elif(scheduler == 'LUHP'):
        lowUtilHighPeriodPriorities(jobSet, taskSet)

    # Task-level:
        # Highest utility higest prio
    # Period-level:
        # Lowest period highest prio
    elif(scheduler == 'HULP'):
        highUtilLowPeriodPriorities(jobSet, taskSet)

    # Task-level:
        # Highest utility higest prio
    # Period-level:
        # Highest period highest prio
    elif(scheduler == 'HUHP'):
        highUtilHighPeriodPriorities(jobSet, taskSet)

    #EDF Priorities
    else:
        edfPriorities(jobSet)

# Lowest utilization overall has highest prio (ignore periods)
def lowUtilPriorities(jobSet, taskSet):

    # Assign prios for R-jobs
    jobList = []
    priority = 1

    # Save all R-jobs
    for job in jobSet.jobs:
        if job.isRestitution():
            jobList.append(job)

    jobList.sort(key=lambda x: x.utilization)
    for job in jobList:
        job.priority = priority
        priority += 1


    # Assign prios for A-jobs
    jobList = []
    
    # Save all A-jobs
    for job in jobSet.jobs:
        if job.isAcquisition():
            jobList.append(job)

    jobList.sort(key=lambda x: x.utilization)
    for job in jobList:
        job.priority = priority
        priority += 1


# Highest utilization overall has highest prio (ignore periods)
def highUtilPriorities(jobSet, taskSet):
    
    # Assign prios for R-jobs
    jobList = []
    priority = 1

    # Save all R-jobs
    for job in jobSet.jobs:
        if job.isRestitution():
            jobList.append(job)

    jobList.sort(key=lambda x: x.utilization, reverse=True)
    for job in jobList:
        job.priority = priority
        priority += 1


    # Assign prios for A-jobs
    jobList = []
    
    # Save all A-jobs
    for job in jobSet.jobs:
        if job.isAcquisition():
            jobList.append(job)

    jobList.sort(key=lambda x: x.utilization, reverse=True)
    for job in jobList:
        job.priority = priority
        priority += 1


#EDF
def edfPriorities(jobSet):
    maxRPrio = 0

    #Assign R-priorities according to EDF
    for job in jobSet.jobs:
        if job.isRestitution():
            job.priority = job.deadline
            maxRPrio = max(maxRPrio, job.priority)


    # No A-phase should have same prio as an R-phase, so add 1 incase a task has a prio of 0
    maxRPrio += 1

    # Assign A-priorities according to their task priority
    # We assign their priority according to deadline (EDF)
    for job in jobSet.jobs:
        if job.isAcquisition():
            job.priority = maxRPrio + job.deadline


# Task-level:
    # Lowest utility highest prio
# Period-level:
    # Lowest period highest prio
def lowUtilLowPeriodPriorities(jobSet, taskSet):

    periods = [10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000]


    # Assign R-job prios
    priority = 1
    jobList = []

    # Iterate periods from low to high
    for period in periods:
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isRestitution():
                    # Jobs is restitution and has desired period
                    jobList.append(job)
                    
        # Now we have all R jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization)
        for job in jobList:
            job.priority = priority
            priority += 1


        #Reset list
        jobList = []


    # Assign A-job prios
    jobList = []

    # Iterate periods from low to high
    for period in periods:
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isAcquisition():
                    # Jobs is acquisition and has desired period
                    jobList.append(job)
                    
        # Now we have all A jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization)
        for job in jobList:
            job.priority = priority
            priority += 1


        #Reset list
        jobList = []


# Task-level:
    # Lowest utility highest prio
# Period-level:
    # Highest period highest prio
def lowUtilHighPeriodPriorities(jobSet, taskSet):

    periods = [10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000]

    # Assign R-job prios
    priority = 1
    jobList = []

    # Iterate periods from low to high
    for period in reversed(periods):
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isRestitution():
                    # Jobs is restitution and has desired period
                    jobList.append(job)
                    
        # Now we have all R jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization)
        for job in jobList:
            job.priority = priority
            priority += 1


        #Reset list
        jobList = []


    # Assign A-job prios
    jobList = []

    # Iterate periods from high to low
    for period in reversed(periods):
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isAcquisition():
                    # Jobs is acquisition and has desired period
                    jobList.append(job)
                    
        # Now we have all A jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization)
        for job in jobList:
            job.priority = priority
            priority += 1

        #Reset list
        jobList = []


# Task-level:
    # Highest utility higest prio
# Period-level:
    # Lowest period highest prio
def highUtilLowPeriodPriorities(jobSet, taskSet):

    periods = [10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000]

    # Assign R-job prios
    priority = 1
    jobList = []

    # Iterate periods from low to high
    for period in reversed(periods):
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isRestitution():
                    # Jobs is restitution and has desired period
                    jobList.append(job)
                    
        # Now we have all R jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization, reverse = True)
        for job in jobList:
            job.priority = priority
            priority += 1


        #Reset list
        jobList = []


    # Assign A-job prios
    jobList = []

    # Iterate periods from low to high
    for period in periods:
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isAcquisition():
                    # Jobs is acquisition and has desired period
                    jobList.append(job)
                    
        # Now we have all A jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in decreasing order
        jobList.sort(key=lambda x: x.utilization, reverse=True)
        for job in jobList:
            job.priority = priority
            priority += 1

        #Reset list
        jobList = []


# Task-level:
    # Highest utility higest prio
# Period-level:
    # Highest period highest prio
def highUtilHighPeriodPriorities(jobSet, taskSet):

    periods = [10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000]

    # Assign R-job prios
    priority = 1
    jobList = []

    # Iterate periods from low to high
    for period in reversed(periods):
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isRestitution():
                    # Jobs is restitution and has desired period
                    jobList.append(job)
                    
        # Now we have all R jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in increasing order
        jobList.sort(key=lambda x: x.utilization, reverse=True)
        for job in jobList:
            job.priority = priority
            priority += 1


        #Reset list
        jobList = []


    # Assign A-job prios
    jobList = []

    # Iterate periods from high to low
    for period in reversed(periods):
        # Iterate jobs of the period
        for job in  jobSet.jobs:
            if job.period == period:
                if job.isAcquisition():
                    # Jobs is acquisition and has desired period
                    jobList.append(job)
                    
        # Now we have all A jobs of a given period in jobList
        # Order list of relevant jobs according to utilization in decreasing order
        jobList.sort(key=lambda x: x.utilization, reverse=True)
        for job in jobList:
            job.priority = priority
            priority += 1

        #Reset list
        jobList = []


# Return the A and R jobs that a single task would produce within a given hyperperiod as a list of lists
def generateJobs(windowRatio):

    taskSet = Task_Set()
    jobSet = Job_Set()

    hyperPeriod = taskSet.getHyperPeriod()

    # Iterate through all tasks
    for task in taskSet.tasks:

        # Amount of jobs to be produced
        jobAmount = int(hyperPeriod / task.period)

        for i in range(jobAmount):
            currentTime = i * task.period

            jobInterval = task.deadline - task.arrival_min  
            windowSize = jobInterval - task.computation_max

            # Create the job ID pair as there are some constraints on how they should be created
            idPair = jobSet.getNextIDPair()

            # Create the A job
            aJob = Job()
            aJob.task_id = task.task_id
            aJob.job_id = idPair[0] 
            aJob.utilization = task.utilization
            #Arrival for A is same as arrival for task
            aJob.arrival_min = currentTime + task.arrival_min
            aJob.arrival_max = currentTime + task.arrival_max
            aJob.cost_min = task.acquisition
            aJob.cost_max = task.acquisition
            aJob.period = task.period

            # The deadline of the A job is given by the window ratio given as input
            absoluteADeadline = ceil(windowRatio * windowSize)
            aJob.deadline = currentTime + absoluteADeadline


            # Create the R job
            rJob = Job()
            rJob.task_id = task.task_id
            rJob.job_id = idPair[1] 
            rJob.utilization = task.utilization
            #Arrival for R is A-window + WCET 
            #Assume deterministic arrival
            #If the split between A and R window isnt an integer the extra cycle is given to the R window.
            rJob.arrival_min = aJob.deadline + task.computation_max
            rJob.arrival_max = rJob.arrival_min
            rJob.cost_min = task.restitution
            rJob.cost_max = task.restitution
            rJob.period = task.period

            # The deadline of the A job is given by the window ratio given as input
            rJob.deadline = currentTime + task.deadline

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
            task.utilization = float(row['utilization'])
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
        self.utilization = None
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

    def getTask(self, taskID):
        for task in self.tasks:
            if task.task_id == taskID:
                return task

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
        self.utilization = None
        self.arrival_min = None
        self.arrival_max = None
        self.cost_min = None
        self.cost_max = None
        self.deadline = None
        self.priority = None
        self.period = None

    def isRestitution(self):
        return not self.isAcquisition()

    def isAcquisition(self):
        return self.job_id % 2

class Job_Set:

    # Static variables
    jobs = []
    # Print job set as csv
    def printJobs(self, out):

        outputFile = open(out, 'w+') if out else sys.stdout

        outputFile.write("Task ID, Job ID, Arrival min, Arrival max, Cost min, Cost max, Deadline, Priority\n")

        for job in self.jobs:
            outputFile.write(str(job.task_id) + "," \
                    + str(job.job_id) + "," \
                    + str(job.arrival_min) + "," \
                    + str(job.arrival_max) + "," \
                    + str(job.cost_min) + "," \
                    + str(job.cost_max) + "," \
                    + str(job.deadline) + "," \
                    + str(job.priority) + "\n")

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
        return not job_id % 2


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

