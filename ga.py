from operator import attrgetter
from parameters import *
from random import randint
from individual import Individual
from functools import reduce


class GA:
    def __init__(
        self, data, expected_result, popsize=50, mut_rate=20, GA_printers=None
    ):
        Individual.expected_result = {"rowdata": expected_result}
        Individual.mutation_rate = mut_rate
        Individual.data = data
        self.popsize = popsize
        self.population = []
        for i in range(0, popsize):
            c = Individual()
            c.randomize()
            self.population.append(c)
        self.population.sort(key=attrgetter("fitness"), reverse=True)
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
        r = randint(0, self.wheel_size - 1)
        self.test[self.wheel[r]] += 1
        return self.population[self.wheel[r]]

    def check_duplicate(self, element):
        h = hash(element)
        count = reduce(lambda a, e: a + (1 if hash(e) == h else 0), self.population, 0)
        return count >= 2

    def randomize_duplicates(self):
        for i in self.population[1:]:
            dup = self.check_duplicate(i)
            if dup:
                i.mutate(True)
                i.randomize()

    def apply_max(self):
        for i in self.population[1:]:
            i.apply_max()

    def evaluate_all(self):
        for i in self.population:
            i.evaluate()

    def run_once(self):
        newpop = []
        # Elitism, keep the best chromosome to the next generation
        newpop = self.population[:3]
        for i in range(3, self.popsize):
            tmpchrom = Individual(mother=self.__my_choice(), father=self.__my_choice())
            tmpchrom.mutate()
            newpop.append(tmpchrom)
        self.population = newpop
        self.evaluate_all()
        self.randomize_duplicates()
        self.apply_max()
        self.evaluate_all()
        self.population.sort(key=attrgetter("fitness"), reverse=True)
        self.inc_mutation_rate(MUTATION_RATE_INC)

    def inc_mutation_rate(self, mutation_rate):
        Individual.mutation_rate += mutation_rate

    def end(self, outfilename):
        self.evaluate_all()
        self.population.sort(key=attrgetter("fitness"), reverse=True)
        best = self.population[0]
        print(best.crits["rowdata"])
        print(best.st())
        print(
            "ratio generation/population_size: %.3f"
            % (self.generation / float(POP_SIZE))
        )
        best.dump(outfilename)

    def run(self, outfilename="best.pickled"):
        try:
            while self.population[0].fitness != 1.0:
                self.run_once()
                for printer in self.GA_printers:
                    printer.refresh_screen(self)
                self.generation += 1
            self.end(outfilename)
        except KeyboardInterrupt:
            self.end(outfilename)


class GA_print_text:
    def refresh_screen(self, ga):
        print(
            "Generation: %d (mutation rate=%d)"
            % (ga.generation, Individual.mutation_rate)
        )
        for i in ga.population[:5]:
            print(i)


def run(data, expected, outfilename):
    a = GA(data, expected, POP_SIZE, MUTATION_RATE, GA_printers=[GA_print_text()])
    a.run(outfilename)


if __name__ == "__main__":
    import sys

    stream = open(sys.argv[1])
    data = stream.read()
    stream = open(sys.argv[2])
    expected = stream.read()
    outfilename = sys.argv[3]
    run(data, expected, outfilename)

