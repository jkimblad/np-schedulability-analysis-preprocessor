#!/usr/bin/env python3

# The unit of the program output is micro seconds due to the periods being used
# are from AUTOSAR. The output can be converted to any suitable time unit.

#Import libraries
import sys
import random
import csv
# numpy is used to create custom discrete distributions
import numpy as np
import argparse

#Constants
EXPECTED_ARGUMENTS = 3
TASK_AMOUNT_ARGUMENT = 1
UTILIZATION_ARGUMENT = 2
MILLISECONDS    = 100
MICROSECONDS    = 100000
NANOSECONDS     = 100000000
TIME_RESOLUTION = NANOSECONDS

#Input arguments
want_aer = False;

# Main, execution starts here
def main():

    # Parse user arguments/options
    inputArguments = inputParse()

    #Save input arguments
    taskAmountArg = int(inputArguments.taskAmount)
    utilizationArg = float(inputArguments.utilization)
    #Save if we should generate AER task set
    if not(inputArguments.arFactors is None):
        want_aer = True

    #Randomise utilizations
    utilizations = uUniFast(taskAmountArg, utilizationArg)

    #Randomize periods, assume periods are equal to deadlines
    periods = generatePeriods(taskAmountArg)
    
    # Generate a regular task set
    if not(want_aer):
        #Calculate computation times
        computationTimes = calculateComputationTimes(periods, utilizations)
    # Generate tasks with A, E and R phases
    else:
        computationTimes = calculateAerComputationTimes(periods, utilizations, inputArguments.arFactors)

    #Randomize release times
    releaseTimes = generateReleaseTimes(taskAmountArg)

    #Randomize priorities
    priorities = generatePriorities(taskAmountArg)

    # Print generate tasks to output
    printTasks(utilizations, periods, computationTimes, releaseTimes, priorities, inputArguments)

    
def calculateAerComputationTimes(periods, utilizations, arFactors):
    bcetList = []
    wcetList = []
    aetList = []
    retList = []

    # Used to translate a period into an index for the bcet and wcet lists
    periodsEnum = {'100' : 0, '200' : 1, '500' : 2, '1000' : 3, '2000' : 4, '5000' : 5, '10000' : 6, '20000' : 7}

    # The following bcet and wcet factors are given by the free real benchmarks for the automotive industry
    # Best-case execution time as intervals of factors of the average case
    bcetFactors = [[0.19, 0.92], [0.12, 0.89], [0.17,  0.94], [0.05, 0.99], [0.11, 0.98], [0.32, 0.95], [0.09, 0.99], [0.45,0.98]]
    # Worst-case execution time as intervals of factors of the average case
    wcetFactors = [[1.30, 29.11], [1.54, 19.04], [1.13, 18.44], [1.06, 30.03], [1.06, 15.61], [1.13, 7.76], [1.02, 8.88], [1.03, 4.90]]

    # Iterate through each period
    for i in range(0, len(periods)):

        bcetMin = bcetFactors[periodsEnum[str(periods[i])]][0] 
        bcetMax = bcetFactors[periodsEnum[str(periods[i])]][1] 

        # For now, use the optimal BCET within the given interval
        bcetFactor = bcetMax
        bcet = int(periods[i] * utilizations[i] * bcetFactor)

        # We do the same for wcet
        # We calculate A and R times from the bcet
        wcetMin = wcetFactors[periodsEnum[str(periods[i])]][0] 
        wcetMax = wcetFactors[periodsEnum[str(periods[i])]][1] 

        # For now, use the optimal WCET within the given interval
        wcetFactor = wcetMin
        wcet = int(periods[i] * utilizations[i] * wcetFactor)

        # For now, same wcet and bcet, as wcet is only interesting part for us
        wcet = int(periods[i] * utilizations[i] * wcetFactor)

        # Calculate A and E from BCET to not overshoot the total execution time
        # (if a + e is close to 1 and calculated from the WCET their sum might
        # be larger than the BCET resulting in a negative BCET in later
        # calculations) 
        
        #Calculate Aqcuisition Execution Time
        aet = int(bcet * float(arFactors[0]))
        # Calculate Restitution Execution Time
        ret = int(bcet * float(arFactors[1]))

        # Remove A and R times from the execution time to maintain the same utilization
        wcet = wcet - (aet + ret)
        bcet = bcet - (aet + ret)

        # Append to all lists
        wcetList.append(wcet)
        bcetList.append(bcet)
        aetList.append(aet)
        retList.append(ret)

    # Return results as a dictionary containing the four lists
    computationTimes = { 'bcet' : bcetList, 'wcet' : wcetList, 'aet' : aetList, 'ret' : retList }
    return computationTimes

def inputParse():
    parser = argparse.ArgumentParser()

    # Output file
    parser.add_argument("-o", "--output", dest="outputFile", help="Output FILE", metavar="FILE")

    # Amount of tasks
    parser.add_argument("taskAmount", help="Amount of tasks to be generated within the task set", metavar="tasks")

    # Desired task set utilization
    parser.add_argument("utilization", help="The desired total utilization of the task set", metavar="util")

    # Create A and R jobs
    parser.add_argument("-a", "--aer", nargs=2, dest="arFactors", help="Input is transformed to A and R jobs to be scheduled onto memory. First argument is the utilization factor of the acquisition phase and the second is the utilization factor of the restitution phase as part of the whole execution time of the task (a+e+r).", metavar="UTIL")

    return parser.parse_args()


def printTasks(utilizations, periods, computationTimes, releaseTimes, priorities, inputArguments):

    # No A and R phases
    if not (inputArguments.arFactors):
        fieldNames = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "deadline", "priority", "period"]

    # A and R phases
    else:
        fieldNames = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "acquisition", "restitution", "deadline", "priority", "period"]

    # Open output file is given, else print to stdout
    outputFile = open(inputArguments.outputFile, 'w+') if inputArguments.outputFile else sys.stdout
    writer = csv.writer(outputFile, fieldNames)
    writer.writerow(fieldNames)

    for i in range(len(utilizations)):
        task = []

        #id
        task.append(i + 1)

        #release
        task.append(releaseTimes['bcrt'][i])
        task.append(releaseTimes['wcrt'][i])

        #computation
        #min
        task.append(computationTimes['bcet'][i])
        #max
        task.append(computationTimes['wcet'][i])

        # Check if we add A and R phases to output
        if(inputArguments.arFactors):
            # Acquisition
            task.append(computationTimes['aet'][i])

            # Restitution
            task.append(computationTimes['ret'][i])

        #deadline
        #deadline equals period
        task.append(periods[i])

        #priority
        #prio is currently rms
        task.append(periods[i])

        #period
        task.append(periods[i])

        writer.writerow(task)


def generatePriorities(taskAmount):
    priorities = list(range(1, taskAmount + 1))
    random.shuffle(priorities)
    return priorities


def generateReleaseTimes(taskAmount):
    # Best Case Release-Time
    bcrt = []
    # Worst Case Release-Time
    wcrt = []
    for i in range (taskAmount):
        # bcrt.append(random.randint(0, 1))
        # wcrt.append(random.randint(1, 2))
        bcrt.append(0)
        wcrt.append(0)

    releaseTimes = {'bcrt' : bcrt, 'wcrt' : wcrt}
    return releaseTimes


def calculateComputationTimes(periods, utilizations):
    bcet = []
    wcet = []

    # Used to translate a period into an index for the bcet and wcet lists
    periodsEnum = {'100' : 0, '200' : 1, '500' : 2, '1000' : 3, '2000' : 4, '5000' : 5, '10000' : 6, '20000' : 7}

    # The following bcet and wcet factors are given by the free real benchmarks for the automotive industry
    # Best-case execution time as intervals of factors of the average case
    bcetFactors = [[0.19, 0.92], [0.12, 0.89], [0.17,  0.94], [0.05, 0.99], [0.11, 0.98], [0.32, 0.95], [0.09, 0.99], [0.45,0.98]]
    # Worst-case execution time as intervals of factors of the average case
    wcetFactors = [[1.30, 29.11], [1.54, 19.04], [1.13, 18.44], [1.06, 30.03], [1.06, 15.61], [1.13, 7.76], [1.02, 8.88], [1.03, 4.90]]

    # Iterate through each period
    for i in range(0, len(periods)):
        bcetMin = bcetFactors[periodsEnum[str(periods[i])]][0] 
        bcetMax = bcetFactors[periodsEnum[str(periods[i])]][1] 

        # For now, use the optimal BCET within the given interval
        bcetFactor = bcetMax
        bcet.append(int(periods[i] * utilizations[i] * bcetFactor))

        # We do the same for wcet
        wcetMin = wcetFactors[periodsEnum[str(periods[i])]][0] 
        wcetMax = wcetFactors[periodsEnum[str(periods[i])]][1] 

        # For now, use the optimal WCET within the given interval
        wcetFactor = wcetMin
        wcet.append(int(periods[i] * utilizations[i] * wcetFactor))

    # Return results as a dictionary containing the two lists
    computationTimes = { 'bcet' : bcet, 'wcet' : wcet }
    return computationTimes
        


# Generate periods of tasks based on real benchmarks
def generatePeriods(taskAmount):
    # These are taken from "Real World Automotive Benchmarks For Free" and
    # adapted (with roundings) due to the fact that we exclude angle-synchronous
    # periods 
    # Periods measured in micro seconds
    periods = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    # periods = [1, 2, 5, 10, 20, 50, 100, 200, 1000]
    # periodDistribution = [0.04, 0.02, 0.02, 0.29, 0.29, 0.04, 0.24, 0.01, 0.05]
    # TOOD: add the 0.05 probability of 1000ms period to others
    periodDistribution = [0.05, 0.03, 0.03, 0.29, 0.29, 0.05, 0.24, 0.02]

    return np.random.choice(periods, taskAmount, p=periodDistribution)


# Utilization randomisation algorithm described in "Measuring the Performance of Schedulability Tests"
def uUniFast(taskAmount, utilization):
    # Classic UUniFast algorithm:
    utilizations = []
    sumU = utilization
    for i in range(1, taskAmount):
        nextSumU = sumU * random.random() ** (1.0 / (taskAmount - i))
        utilizations.append(sumU - nextSumU)
        sumU = nextSumU

    utilizations.append(sumU)

    return utilizations


if __name__ == '__main__':
    main()


