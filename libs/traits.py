from random import randint
import sys

class Trait(object):
    value = None

    def mutate(self):
        raise Exception("Your trait must implement the `mutate` method.")

    def copy(self):
        instance = self.__class__()
        instance.value = self.value
        return instance
    

class IntegerTrait(Trait):
    int_min = 0
    int_max = 0xff

    delta = 100 

    def __init__(self, n=None):
        if not n:
            self.value = randint(self.int_min, self.int_max)

        else:
            self.value = n

    def mutate(self):
        self.value += randint(-self.delta, self.delta) 

        if self.value > self.int_max:
            self.value = self.int_max

        if self.value < self.int_min:
            self.value = self.int_min
