from parameters import *
from compare_parsed import compare_criterias
from random import randint, choice
from primitives import str_primitives, re_primitives, clean_primitives
from baseparser import BaseParser
from operator import attrgetter

class Individual(BaseParser):
    expected_result = {}
    mutation_rate = 0

    max_str = MAX_STR
    max_s2l = MAX_S2L
    max_clean = MAX_CLEAN

    def __init__(self, mother=None, father=None):
        BaseParser.__init__(self)
        if mother and father:
            self.crossover(mother, father)
        else:
            self.fitness = 0

    def constraints(self):
        todel = []
        for n, i in enumerate(zip(self._s2l_ops, self._s2l_ops[1:])):
            if i[0][1] == 0 and i[1][1] == 0:
                todel.append(n)
        for n, i in enumerate(todel):
            del self._s2l_ops[i - n]

    def randomize(self):
        for i in range(randint(0, self.max_str)):
            self._str_ops.append(choice(str_primitives))
        for i in range(randint(1, self.max_s2l)):
            self._s2l_ops.append(choice(re_primitives))
        for i in range(randint(0, self.max_clean)):
            self._clean_ops.append(choice(clean_primitives))
        self.constraints()

    def crossover_list(self, l1, l2):
        crossover_point = randint(0, min(len(l1), len(l2)))
        return l1[crossover_point:] + l2[:crossover_point]

    def apply_max(self):
        self._str_ops = self._str_ops[:self.max_str]
        self._s2l_ops = self._s2l_ops[:self.max_s2l]
        self._clean_ops = self._clean_ops[:self.max_clean]

    def crossover(self, mother, father):
        self._str_ops = self.crossover_list(mother._str_ops, father._str_ops)
        self._s2l_ops = self.crossover_list(mother._s2l_ops, father._s2l_ops)
        self._clean_ops = self.crossover_list(mother._clean_ops,
                                              father._clean_ops)
        self.constraints()

    def mutate_list(self, l, all):
        r = randint(0, 100)
        if len(l) == 0:
            i, r = 0, 0
        else:
            i = randint(0, len(l) - 1)
        if r < 10: # add
            l.insert(i, choice(all))
        elif r > 90: # delete
            del l[i]
        else: #modify
            l[i] = choice(all)

    def mutate(self):
        test = randint(0, 100)
        if test < self.mutation_rate:
            r = randint(0, 2)
            if r == 0:
                self.mutate_list(self._str_ops, str_primitives)
            elif r == 1:
                self.mutate_list(self._s2l_ops, re_primitives)
            else:
                self.mutate_list(self._clean_ops, clean_primitives)
        self.constraints()

    def evaluate(self):
        self.run_all()
        c = self.criterias()
        self.fitness = compare_criterias(self, self.expected_result)

    def __cmp__(self, o):
        return cmp(self.fitness, o.fitness)

    def __str__(self):
        return str(round(self.fitness, 5)) #+ ":" + self.st() #+ ":" + str(self.parsed)

if __name__ == "__main__":
    pass

