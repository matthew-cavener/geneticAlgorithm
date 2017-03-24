print('\n\n\nInitializing-------------------------------')

import string

from timeit import default_timer
from random import choice
from random import random
from random import randint
# from bisect import bisect
# from itertools import accumulate

startTime = default_timer()
print('\n\n\n')

targetString = 'This is the target string. The quick Brown Fox jumps over the lazy yellow dog. I do not really think that is the right sentence, but I am too lazy too look it up, and really just needed some character so solve for.'
genomeLength = len(targetString)
populationSize = 500
tournamentSize = 5
mutationRate = 0.99
stopAfterThisManyGenerations = 10000
generationsToWatch = 1
populationOutputFile = open("finalPopulation.txt", "w")
InitialPopulationOutputFile = open("initialPopulation.txt", "w")


def generateGenome(genomeLength):

    return ''.join([choice(list(string.printable + string.digits)) for _ in range(genomeLength)])


def generateInitialPopulation(populationSize):

    return [generateGenome(genomeLength) for _ in range(populationSize)]


def individualFitnessTest(genome):

    fitnessScore = 0

    for i in range(genomeLength):
        if genome[i] == targetString[i]:
            fitnessScore += 1

    return float(fitnessScore)


def populationFitnessTest(population):

    return (map(individualFitnessTest, population))


def generateFitnessFractions(populationFitnessScores):

    totalPopulationFitness = sum(populationFitnessScores)

    return map(lambda fitnessScore: fitnessScore / totalPopulationFitness, populationFitnessScores)


def generateReproductionTable(fitnessFractions):

    reproductionTable = []
    total = 0

    for f in fitnessFractions:
        total = total + f
        reproductionTable.append(total)

    return reproductionTable


'''
def selectParent(population, reproductionTable):

    return population[bisect(reproductionTable, random())]
'''


# def elitism(population, populationFitnessScores):
	

def selectParent(population, populationFitnessScores):

    tournament = []
    tournamentFitnessScores = []

    for i in range(0, tournamentSize):

        selectedIndividualIndex = randint(0, populationSize - 1)

        tournament.append(''.join(population[selectedIndividualIndex]))
        tournamentFitnessScores.append(populationFitnessScores[selectedIndividualIndex])

    tournamentWinner = tournamentFitnessScores.index(max(tournamentFitnessScores))
    return tournament[tournamentWinner]



'''
def selectSecondParent(population, populationFitnessScores, firstParent):

    neighborhood = []

    for i in range(firstParent - 5, firstParent):
        neighborhood.append(population[i % populationSize])

    for i in range(firstParent + 1, firstParent + 6):
        neighborhood.append(population[i % populationSize])

    return max(neighborhood)
'''


def generateChild(population, populationFitnessScores):

    firstParent = list(selectParent(population, populationFitnessScores))
    secondParent = list(selectParent(population, populationFitnessScores))

    while firstParent == secondParent:
        secondParent = list(selectParent(population, populationFitnessScores))

    child = secondParent

    for i in range(int(genomeLength / 2)):
        geneToSwitch = randint(0, genomeLength - 1)
        child[geneToSwitch] = firstParent[geneToSwitch]

    return ''.join(child)


def generateNewPopulation(population, populationFitnessScores):

    # fitnessFractions = generateFitnessFractions(populationFitnessScores)
    # reproductionTable = generateReproductionTable(fitnessFractions)

    return [generateChild(population, populationFitnessScores) for _ in range(populationSize)]


def mutate(population, numberOfGenerations):
    for i in range(populationSize):

        if random() < (mutationRate * 1):

            mutatedMember = list(population[i])
            mutatedMember[randint(0, genomeLength - 1)] = choice(list(string.printable + string.digits))
            population[i] = ''.join(mutatedMember)

    return population


def evolve(population):

    numberOfGenerations = 1

    populationFitnessScores = populationFitnessTest(population)
    indexOfMostFitMember = populationFitnessScores.index(max(populationFitnessScores))
    mostFitMember = population[indexOfMostFitMember]
    similarityToTargetString = (populationFitnessScores[indexOfMostFitMember] / genomeLength)

    print('Generations elapsed:           ' + str(numberOfGenerations) + '===========================================================')
    print('Current most fit member:       ' + ''.join(mostFitMember))
    print('Percent similarity to target:  ' + str(round(similarityToTargetString, 4) * 100) + '%')
    print('\n\n\n')

    while numberOfGenerations < stopAfterThisManyGenerations:


        populationFitnessScores = populationFitnessTest(population)
        indexOfMostFitMember = populationFitnessScores.index(max((populationFitnessScores)))
        mostFitMember = population[indexOfMostFitMember]
        similarityToTargetString = (populationFitnessScores[indexOfMostFitMember] / genomeLength)

        if mostFitMember == targetString:
            print('The number of generations elapsed was ' + str(numberOfGenerations))
            populationOutputFile.write('\n\n\n'.join(population))
            populationOutputFile.close()
            return ((mostFitMember))

        population = generateNewPopulation(population, populationFitnessScores)
        mutate(population, numberOfGenerations)
        numberOfGenerations = numberOfGenerations + 1


        if numberOfGenerations % generationsToWatch == 0:


            print('Generations elapsed:           ' + str(numberOfGenerations) + '===========================================================')
            print('Current most fit member:       ' + ''.join(mostFitMember))
            print('Percent similarity to target:  ' + str(round(similarityToTargetString, 4) * 100) + '%')
            print('\n\n\n')

        if mostFitMember == targetString:
            print('The number of generations elapsed was ' + str(numberOfGenerations))
            populationOutputFile.write('\n\n\n'.join(population))
            populationOutputFile.close()
            return ((mostFitMember))

    print('The number of generations elapsed was ' + str(numberOfGenerations + 1))
    populationOutputFile.write('\n\n\n'.join(population))
    populationOutputFile.close()
    return ((mostFitMember))

initialPopulation = generateInitialPopulation(populationSize)
InitialPopulationOutputFile.write('\n\n\n'.join(initialPopulation))
InitialPopulationOutputFile.close()

print(evolve(initialPopulation))









'''
# ============================ Testing Stuff is Below / may contain old nonfunctional code ====================================== #
initialPopulation = generateInitialPopulation(5)
populationFitnessScores = populationFitnessTest(initialPopulation)
fitnessFractions = generateFitnessFractions(populationFitnessScores)
reproductionTable = generateReproductionTable(fitnessFractions)

print(initialPopulation)
print(reproductionTable)
print('\n\n\n\n')

print(selectFirstParent(reproductionTable))
'''


timeTaken = str(round(default_timer() - startTime, 3))
print('Program run time was ' + timeTaken + ' seconds.')
