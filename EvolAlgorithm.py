# -*- coding: utf-8 -*-

from Popul import Popul


class EvolAlgorithm:

    def __init__(self, popsize, numits, noffspring, indsize, elitism = 0):
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize
        if elitism != 0 and elitism <= (self.popsize - self.noffspring):
            self.elitism = elitism
        else:
            self.elitism = 0

    def initPopul(self, indsize):
        self.popul = Popul(self.popsize, indsize, elitism=self.elitism)

    def iteration(self):
        parents = self.popul.selection(self.noffspring)
        offspring = self.popul.recombination(parents, self.noffspring)
        self.evaluate(offspring)
        self.popul.reinsertion(offspring)

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():
                if x == 1:
                    fit += 1.0
            ind.setFitness(fit)
        return None

    def run(self):
        self.initPopul(self.indsize)
        self.evaluate(self.popul.indivs)
        self.bestsol = []
        self.bestfit = 0.0
        for i in range(self.numits+1):
            self.iteration()
            bs, bf = self.popul.bestSolution()
            if bf > self.bestfit:
                self.bestfit = bf
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.popul.bestFitness())
        #self.bestsol, self.bestfit = self.popul.bestSolution()


def test():
    ea = EvolAlgorithm(100, 2000, 50, 1000, 20)
    ea.run()


if __name__ == "__main__":
    test()
