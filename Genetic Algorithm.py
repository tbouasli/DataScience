# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Genetic Algorithm

# %%
import numpy as np
import random
import string
from IPython.display import display, clear_output
import time
import sys
import os

def clear_output_os():
    # Clear the output screen
    os.system('cls' if os.name == 'nt' else 'clear')
# %%
class DNA:
    def __init__(self, target):
        self.target = target
        self.genes = self.randomCharList(target)
        self.fitness = 0

    def randomCharList(self ,target):
        return [random.choice(string.ascii_letters + ' ') for _ in range(len(target))]

    def calculateFitness(self):
        score = 0
        for i in range(len(self.target)):
            if self.genes[i] == self.target[i]:
                score += 1
        self.fitness = score / len(self.target)

    def reproduce(self, partner):
        child = DNA(self.target)
        midpoint = int(random.random() * len(self.genes))
        child.genes = self.genes[0:midpoint] + partner.genes[midpoint:]
        return child

    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if random.random() < mutationRate:
                self.genes[i] = random.choice(string.ascii_letters + ' ')
    def getPhrase(self):
        return ''.join(self.genes)


# %%
class Population:
    def __init__(self, size, target):
        self.size = size
        self.individuals = []
        self.target = target
        self.generation = 0
        self.create()

    def create(self):
        for _ in range(self.size):
            self.individuals.append(DNA(self.target))

        self.mutate()

    def mutate(self):
        for individual in self.individuals:
            individual.mutate(0.01)

    def evaluate(self):
        for individual in self.individuals:
            individual.calculateFitness()

    def reproduce(self):
        matingPool = MatingPool(self.individuals)
        matingPool.create()
        matingPool.select()
        nextGen = matingPool.reproduce()
        self.individuals = nextGen
        self.mutate()
        self.generation += 1

    def getBest(self):
        best = self.individuals[0]
        for individual in self.individuals:
            if individual.fitness > best.fitness:
                best = individual
        return best

    def getBestPhrase(self):
        return self.getBest().getPhrase()
        

    
    


# %%
class MatingPool:
    def __init__(self, population):
        self.population = population
        self.matingPool = []
        self.reproductionCycles = 1000

    def create(self):
        for individual in self.population:
            for _ in range(int(individual.fitness * 100)):
                self.matingPool.append(individual)

    def select(self):
        return random.choice(self.matingPool)

    def reproduce(self):
        children = []
        for _ in range(self.reproductionCycles):
            parentA = self.select()
            parentB = self.select()
            child = parentA.reproduce(parentB)
            children.append(child)
        return children


# %%
class Evolution:

    def __init__(self, target, populationSize):
        self.target = target
        self.population = Population(populationSize, target)

    def run(self):
        while True:

            display('fittest: ' + str(self.population.getBestPhrase()) + ' | Generation: ' + str(self.population.generation))

            if(self.population.getBestPhrase() == self.target):
                break

            self.population.evaluate()
            self.population.reproduce()
            clear_output(wait=True)
            clear_output_os()
            time.sleep(0.01)


# %%
env = Evolution(sys.argv[1], int(sys.argv[2]))
env.run()

