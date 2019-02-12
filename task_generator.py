#!/usr/bin/env python3

# The unit of the program output is micro seconds due to the periods being used
# are from AUTOSAR. The output can be converted to any suitable time unit.

#Import libraries
import sys
import random
import csv
# numpy is used to create custom discrete distributions
import numpy as np

#Constants
EXPECTED_ARGUMENTS = 3
TASK_AMOUNT_ARGUMENT = 1
UTILIZATION_ARGUMENT = 2


# Main, execution starts here
def main():

    # Check input arguments
    if(len(sys.argv) != EXPECTED_ARGUMENTS):
        print("Expected exactly " + str(EXPECTED_ARGUMENTS - 1) + " arguments, " + str(len(sys.argv) - 1) + " was provided")
        sys.exit()

    #Save input arguments
    taskAmountArg = int(sys.argv[TASK_AMOUNT_ARGUMENT])
    utilizationArg = float(sys.argv[UTILIZATION_ARGUMENT])

    #Randomise utilizations
    utilizations = uUniFast(taskAmountArg, utilizationArg)
    # print (utilizations)

    #Randomize periods, assume periods are equal to deadlines
    periods = generatePeriods(taskAmountArg)
    # print(periods)

    #Calculate computation times
    computationTimes = calculateComputationTimes(periods, utilizations)
    # print (computationTimes['bcet'])
    # print (computationTimes['wcet'])

    #Randomize release times
    releaseTimes = generateReleaseTimes(taskAmountArg)

    #Randomize priorities
    priorities = generatePriorities(taskAmountArg)
    # print(priorities)

    printTasks(utilizations, periods, computationTimes, releaseTimes, priorities)
    
def printTasks(utilizations, periods, computationTimes, releaseTimes, priorities):

    fieldNames = ["id", "arrival_min", "arrival_max", "computation_min", "computation_max", "deadline", "priority", "period"]
    writer = csv.writer(sys.stdout, fieldNames)
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

        #deadline
        #deadline equals period
        task.append(periods[i])

        #priority
        #prio is currently rms
        task.append(periods[i])

        #period
        task.append(periods[i])

        writer.writerow(task)


def generateAcquisitionTimes(taskAmount):
    # Acquisition times is represented as nS
    # These times are acquired from real world examples presented in
    # "Scheduling Multi-Rate Real-Time Applications on Clustered
    # Many-Core Architectures with Memory Constraints"
    codeAcquisitionTimes = [11970, 15543, 12070, 13188, 14858, 12140, 15413, 27593, 15413, 27593, 27730, 15058, 14948, 30470, 14948, 30470, 14945, 14858, 12130, 15300]
    labelAcquisitionTimes = [908, 958, 908, 908, 55, 990, 1013, 990, 1013, 1148, 1060, 988, 965, 933, 908, 28, 985]

    acquisitionTimes = []

    for i in range(taskAmount):
        codeAcquisitionTime = codeAcquisitionTimes[random.randint(0, len(codeAcquisitionTimes) - 1)]
        labelAcquisitionTime = labelAcquisitionTimes[random.randint(0, len(labelAcquisitionTimes) - 1)]
        acquisitionTimes.append(codeAcquisitionTime + labelAcquisitionTime)

    return acquisitionTimes


def generateRestitutionTumes(taskAmount):
    # Restitution times is represented as nS
    # These times are acquired from real world examples presented in
    # "Scheduling Multi-Rate Real-Time Applications on Clustered
    # Many-Core Architectures with Memory Constraints"
    restitutionTimes = [25, 195, 28, 55, 55, 28, 55, 83, 55, 83, 28, 25, 28, 390, 240, 0, 28, 195]

    restitutions = []

    for i in range(taskAmount):
        restitutions.append(restitutionTimes[random.randint(0, len(restitutionTimes) - 1)])

    return restitutions


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
        bcrt.append(random.randint(0, 1))
        wcrt.append(random.randint(1, 2))

    releaseTimes = {'bcrt' : bcrt, 'wcrt' : wcrt}
    return releaseTimes


def calculateComputationTimes(periods, utilizations):
    bcet = []
    wcet = []

    # Used to translate a period into an index for the bcet and wcet lists
    periodsEnum = {'100' : 0, '200' : 1, '500' : 2, '1000' : 3, '2000' : 4, '5000' : 5, '10000' : 6, '20000' : 7, '100000' : 8}

    # The following bcet and wcet factors are given by the free real benchmarks for the automotive industry
    # Best-case execution time as intervals of factors of the average case
    bcetFactors = [[0.19, 0.92], [0.12, 0.89], [0.17,  0.94], [0.05, 0.99], [0.11, 0.98], [0.32, 0.95], [0.09, 0.99], [0.45,0.98], [0.68, 0.80]]
    # Worst-case execution time as intervals of factors of the average case
    wcetFactors = [[1.30, 29.11], [1.54, 19.04], [1.13, 18.44], [1.06, 30.03], [1.06, 15.61], [1.13, 7.76], [1.02, 8.88], [1.03, 4.90], [1.84, 4.75]]

    # Iterate through each period
    for i in range(0, len(periods)):
        # TODO Randomize bcet from interval using some probability distribution
        # The distribution for bcet should however be flipped (more higher
        # values that are closer to the acet)

        bcetMin = bcetFactors[periodsEnum[str(periods[i])]][0] 
        bcetMax = bcetFactors[periodsEnum[str(periods[i])]][1] 
        bcetRange = bcetMax - bcetMin

        # For now, use the optimal BCET within the given interval
        bcetFactor = bcetMax
        bcet.append(int(periods[i] * utilizations[i] * bcetFactor))

        # We do the same for wcet
        wcetMin = wcetFactors[periodsEnum[str(periods[i])]][0] 
        wcetMax = wcetFactors[periodsEnum[str(periods[i])]][1] 
        wcetRange = wcetMax - wcetMin

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
    periods = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 100000]
    # periods = [1, 2, 5, 10, 20, 50, 100, 200, 1000]
    periodDistribution = [0.04, 0.02, 0.02, 0.29, 0.29, 0.04, 0.24, 0.01, 0.05]

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


