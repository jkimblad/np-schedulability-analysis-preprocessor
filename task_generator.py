#Import libraries
import sys
import random
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
    print (utilizations)

    #Randomize periods, assume periods are equal to deadlines
    periods = generatePeriods(taskAmountArg)
    print(periods)

    #Calculate computation times
    computationTimes = calculateComputationTimes(periods, utilizations)
    print (computationTimes)

    #Randomize release times
    releaseTimes = generateReleaseTimes(taskAmountArg)

    #Randomize priorities
    priorities = generatePriorities(taskAmountArg)


def generatePriorities(taskAmount):
    None


def generateReleaseTimes(taskAmount):
    None


def calculateComputationTimes(periods, utilizations):
    computationTimes = []
    for i in range(0, len(periods)):
        computationTimes.append(int(periods[i] * utilizations[i]))

    return computationTimes
        


# Generate periods of tasks based on 
def generatePeriods(taskAmount):
    # These are taken from "Real World Automotive Benchmarks For Free" and
    # adapted (with roundings) due to the fact that we exclude angle-synchronous
    # periods 
    # Periods measured in ns
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

