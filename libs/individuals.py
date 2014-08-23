from .traits import Trait
import random

class Individual(object):
    traits = {}
    crossover_threshold = 0.5
    mutation_chance = 0.05
    single_trait_mutation = False

    def __init__(self, traits={}):
        if len(traits):
            for trait in traits:
                if not isinstance(traits.get(trait), Trait):
                    raise Exception("The Individual constructor needs instances, not classes.")

            self.traits = traits

        else:
            instances = {}
            for trait in self.traits:
                instances[trait] = self.traits[trait]()

            self.traits = instances

        self.numtraits = len(self.traits)


    def __repr__(self):
        def trait_dict_repr(d):
            return dict(zip(d.keys(), [v.__class__.__name__ for v in d.values()]))

        return "<Individual (species='%s', traits=%s, fitness=%d)>" % (
            self.__class__.__name__, trait_dict_repr(self.traits), self.fitness()) 
    
    def __cmp__(self, other):
        return cmp(self.fitness(), other.fitness())

    def __getitem__(self, trait):
        return self.traits[trait].value
    
    def __add__(self, other):
        return self.mate(other)

    def copy(self):
        traits = {}
        for name, trait in self.traits.iteritems():
            traits[name] = trait.copy()

        instance = self.__class__(traits=traits)
        instance.crossover_threshold = self.crossover_threshold
        instance.mutation_chance = self.mutation_chance
        instance.single_trait_mutation = self.single_trait_mutation

        return instance

    def fitness(self):
        raise Exception("You haven't implemented the `fitness` method.")

    def mutate(self):
        mutant = self.copy()

        if self.single_trait_mutation:
            trait = random.choice(mutant.traits.keys())
            mutant.traits[trait].mutate()

        else:
            for trait in mutant.traits:
                if random.random() < self.mutation_chance:
                    mutant.traits[trait].mutate()
    
        return mutant
    
    def mate(self, other):
        traits = {}
        for name, trait in self.traits.iteritems():
            mygene = trait
            theirgene = other.traits.get(name, trait.__class__())

            if random.random() < self.crossover_threshold:
                traits[name] = mygene

            else:
                traits[name] = theirgene

        return self.__class__(traits=traits)
