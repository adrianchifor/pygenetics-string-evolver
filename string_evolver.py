from libs.traits import IntegerTrait
from libs.individuals import Individual
from libs.biosphere import Biosphere

TARGET = raw_input("String to evolve: ");

class GuesserTrait(IntegerTrait):
    int_min = 0 
    int_max = 255 
    delta = 5 

class StringGuesser(Individual):
    traits = traits
    mutation_chance = 0.15
    single_trait_mutation = True 

    def __repr__(self):
        chars = []
        for k in xrange(self.numtraits):
            n = self[str(k)]
            c = str(chr(n))
            chars.append(c)

        return ''.join(chars)

    def fitness(self):
        diffs = 0
        for i in xrange(self.numtraits):
            x0 = ord(TARGET[i])
            x1 = self[str(i)]
            diffs += (x1 - x0) ** 2

        return diffs 

class GuesserBiosphere(Biosphere):
    species = StringGuesser
    specimens = 100
    nfittest = 15
    new_children = 50
    survival = 3 


traits = {}
for c in range(len(TARGET)):
    traits[str(c)] = GuesserTrait

def main():
    biosphere = GuesserBiosphere()
    
    i = 0
    while True:
        best = biosphere.best()
        print "Generation %d: %s   Best = %d" % (
            i, best, best.fitness())
        
        if best.fitness() <= 0:
            print "Woot! Got it!"
            break

        i += 1
        biosphere.evolve()

    raw_input("Press any key to exit...")

if __name__ == '__main__':
    main()
