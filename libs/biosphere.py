from .individuals import Individual 
from .utils import weighted_choice
import random

class Biosphere(object):
    species = Individual
    specimens = 10
    new_specimens = 10
    new_children = 50
    mutant_ratio = 0.1
    nfittest = 10
    survival = 10

    mutant_progeny = True
    
    population = []

    sorted = False


    def __init__(self, *args, **kw):
        self.population = []

        for _ in range(self.specimens):
            self.add(self.species(*args, **kw))
    
    def __getitem__(self, n):
        self.sort()
        return self.population[n]

    def __len__(self):
        return len(self.population)

    def best(self):
        self.sort()
        return self[0]

    def get_fitnesses(self, group):
        fitnesses = []
        for individual in group:
            fitnesses.append(individual.fitness())
       
        return fitnesses 

    def add(self, individual):
        self.population.append(individual) 

    def evolve(self):
        #Introduce new specimens into the biosphere.
        if self.new_specimens:
            for _ in range(self.new_specimens):
                self.add(self.species())

        self.sort()
        children = []
        
        #Mate the specimens, favouring the fittest.
        weights = self.get_fitnesses(self.population)
        for _ in xrange(self.new_children):
            id1 = id2 = weighted_choice(weights)

            while id1 == id2:
                id2 = weighted_choice(weights)

            adult1, adult2 = self[id1], self[id2]
            result = adult1 + adult2

            if self.mutant_progeny:
                result = result.mutate()

            children.append(result)
       
        if self.survival:
            children.extend(self[:self.survival])
       
        if not self.mutant_progeny: 
            weights = self.get_fitnesses(children) 
            mutants = int(self.mutant_ratio * len(children))
            for _ in xrange(mutants):
                i = weighted_choice(weights)
                children.append(children[i].mutate())
       
        #Kill the parents; replace the population with the offspring.
        children.sort()
        self.population = children[:self.nfittest]
        self.sorted = False
        self.sort()

    def sort(self):
        if not self.sorted:
            self.population.sort()
            self.sorted = True
