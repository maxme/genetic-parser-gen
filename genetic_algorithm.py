from simulating_the_simulator import test_func
import random
import math
from functools import reduce


class Chromosome:
    domains = []
    size = 0

    def __init__(
        self,
        domains=[],
        expected_result=0,
        genes=None,
        mutation_rate=20,
        mother=None,
        father=None,
    ):
        if mother and father:
            self.__crossover(mother, father)
        else:
            self.domains = domains
            self.fitness = 0
            self.mutation_rate = mutation_rate
            self.expected_result = expected_result
            if genes == None:
                self.randomize()
            else:
                self.genes = genes

    @property
    def set_domains(self, doms):
        self.domains = doms
        self.size = len(self.domains)

    def randomize(self):
        """
        Construct new genes randomly from the domains
        """

        self.genes = []
        for domain in self.domains:
            self.genes.append(random.uniform(*domain))
        self.evaluate()

    def __crossover(self, mother, father):
        """
        Simple point crossover
        """
        self.mutation_rate = mother.mutation_rate
        self.expected_result = mother.expected_result
        crossover_point = random.randint(0, self.size)
        self.genes = mother.genes[:crossover_point]
        self.genes += father.genes[crossover_point:]
        self.evaluate()

    def mutate(self):
        test = random.randint(1, 100)
        if test < self.mutation_rate:
            n = random.randint(0, self.size)
            self.genes[n] = random.uniform(*domains[n])
            self.evaluate()

    def __str__(self):
        return str(self.genes) + ": " + str(self.fitness)

    def evaluate(self):
        self.fitness = abs(test_func(self.genes) - self.expected_result)

    def __cmp__(self, o):
        return cmp(self.fitness, o.fitness)


class GA:
    def __init__(self, domains, expected_result, popsize=50, GA_printers=None):
        self.popsize = popsize
        self.population = []
        for i in range(0, popsize):
            c = Chromosome(domains, expected_result)
            self.population.append(c)
        self.population.sort()
        self.GA_printers = GA_printers
        self.generation = 0
        self.wheel_size = sum(range(1, popsize + 1))
        self.wheel = []
        self.__init_wheel()
        self.test = [0 for i in range(0, self.popsize)]

    def __str__(self):
        return reduce(lambda x, y: str(x) + "\n" + str(y), self.population)

    def __init_wheel(self):
        for i in range(0, self.popsize):
            for j in range(0, self.popsize - i):
                self.wheel.append(i)

    def __my_choice(self):
        r = random.randint(0, self.wheel_size - 1)
        self.test[self.wheel[r]] += 1
        return self.population[self.wheel[r]]

    def run_once(self):
        newpop = []
        # Elitism, keep the best chromosome to the next generation
        newpop.append(self.population[0])
        for i in range(1, self.popsize):
            # Selection and Crossover
            tmpchrom = Chromosome(mother=self.__my_choice(), father=self.__my_choice())
            tmpchrom.mutate()
            newpop.append(tmpchrom)
        self.population = newpop
        self.population.sort()

    def inc_mutation_rate(self, mutation_rate):
        for chromose in self.population:
            chromose.mutation_rate += mutation_rate

    def run(self):
        while 1:
            self.run_once()
            for printer in self.GA_printers:
                printer.refresh_screen(self.population, self.generation)
            self.generation += 1


class GA_print_text:
    def refresh_screen(self, population, generation):
        print("Generation:", generation)
        for i in population[:5]:
            print(i)


if __name__ == "__main__":
    domains = [(1, 4), (0, 2), (1, 2), (1, 4), (0, 2), (1, 2), (1, 4), (0, 2)]
    a = GA(
        domains,  # domains of input parameters
        8,  # observed result
        200,  # population size
        GA_printers=[GA_print_text()],
    )
    a.run()
