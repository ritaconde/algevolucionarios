from random import randint, random, shuffle, choice
from abc import ABC, abstractmethod


class Indiv():

    def __init__(self, size, genes=[], lowerLim=0, upperLim=1):
        self.lowerLim = lowerLim
        self.upperLim = upperLim
        self.genes = genes
        if not self.genes:
            self.initRandom(size)

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, 1))

    ###
    # Aplica uma mutação de troca entre elementos, ie, pegando em duas posicoes aleatorias (p1<p2), troca os valores dessas posições
    ###
    def swapMutation(self):
        size = len(self.genes)
        pos1 = randint(0, size-2)
        pos2 = randint(pos1+1, size-1)

        genepos1 = self.genes[pos1]
        self.genes[pos1] = self.genes[pos2]
        self.genes[pos2] = genepos1

    ###
    # Aplica uma mutação aleatória entre um intervalo de posições, ie, pegando em duas posicoes aleatorias (p1<p2), troca os valores entre as posicoes no intervalo [p1-p2]
    # de forma aleatória
    ###
    def scrambleMutation(self):
        size = len(self.genes)
        pos1 = randint(0, size-2)
        pos2 = randint(pos1+1, size-1)

        # lista de posicoes entre os dois pontos
        list_pos = list(range(pos1, pos2))
        # lista de posicoes nao usadas entre dois pontos
        list_pos_unused = list(range(pos1, pos2))

        for i in range(len(list_pos)):
            # seleciona da lista de nao usados a posicao de forma aleatoria
            pos_selected = choice(list_pos_unused)

            # remove da lista de nao usados a posicao retornada anteriormente
            list_pos_unused.remove(pos_selected)

            # posicao a alterar selecionada do ponto atual do ciclo na lista de posicoes
            pos_to_change = list_pos[i]

            # altera o valor no self.genes
            self.genes[pos_to_change] = self.genes[pos_selected]

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    def crossover(self, indiv2):
        return self.discrete_crossover(indiv2)

    ###
    # Aplica uma recombinação discreta entre dois individuos através da seleção aleatória de qual dos pais irá selecionar o gene
    ###
    def discrete_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []
        size = len(self.genes)

        genesPai1 = self.genes
        genesPai2 = indiv2.getGenes()

        randomOffS1 = []
        randomOffS2 = []

        # Criar 2 listas binárias para selecionar
        for i in range(size):
            randomOffS1.append(randint(0, 1))
            randomOffS2.append(randint(0, 1))

        # Preenche descendentes com genes dos pais, se 0 pai1, se 1 pai2, para cada posicao
        # Descendente 1
        for i,k in enumerate(randomOffS1):
            if k == 0:
                offsp1.append(genesPai1[i])
            else:
                offsp1.append(genesPai2[i])

        # Descendente 2
        for i,k in enumerate(randomOffS2):
            if k == 0:
                offsp2.append(genesPai1[i])
            else:
                offsp2.append(genesPai2[i])

        return self.__class__(size, offsp1, self.lowerLim, self.upperLim), self.__class__(size, offsp2, self.lowerLim, self.upperLim)

    ###
    # Aplica uma recombinação entre dois individuos através da seleção de um ponto aleatório.
    # Gerando os dois descendentes desde esse ponto o tamanho da lista de genes para frente (desc 1) e para trás (desc 2)     
    ###
    def ring_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []
        size = len(self.genes)

        # Seleciona ponto aleatoriamente
        pos = randint(0, size-1)

        # Junta os genes dos dois indivs ind1+ind2
        joined_genes = self.genes + indiv2.getGenes()
        size_joined_genes = len(joined_genes)

        # Primeiro descendente entre posicao aleatoria + tamanho da lista de genes
        offsp1 = joined_genes[pos:pos+size]

        # Cabeça da lista de sobra
        head = joined_genes[:pos]
        # Cauda da lista de sobra
        tail = joined_genes[pos+size:size_joined_genes]

        # Segundo descendente é igual a concat head+tail na ordem contraria de cada um
        reversed_head = list(reversed(head))
        reversed_tail = list(reversed(tail))
        offsp2 = reversed_head + reversed_tail
        
        return self.__class__(size, offsp1, self.lowerLim, self.upperLim), self.__class__(size, offsp2, self.lowerLim, self.upperLim)

    def one_pt_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0, s-1)
        for i in range(pos):
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        return self.__class__(s, offsp1, self.lowerLim, self.upperLim), self.__class__(s, offsp2, self.lowerLim, self.upperLim)

    def uniform_crossover(self, indiv2):
        if len(self.genes) != len(indiv2.genes):
            return False
        randomG = []
        size = len(self.genes)
        for i in range(len(self.genes)):
            randomG.append(randint(0, 1))
        offsp1 = []
        offsp2 = []
        for k in range(len(randomG)):
            if randomG[k] == 0:
                offsp1.append(self.genes[k])
                offsp2.append(indiv2.genes[k])
            else:
                offsp1.append(indiv2.genes[k])
                offsp2.append(self.genes[k])
        
        return self.__class__(size, offsp1), self.__class__(size, offsp2)

class IndivInt (Indiv):

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.upperLim))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = randint(0, self.upperLim)


class IndivReal (Indiv):

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            delta = self.upperLim-self.lowerLim
            self.genes.append(random()*delta+self.lowerLim)

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        delta = self.upperLim-self.lowerLim
        self.genes[pos] = random()*delta+self.lowerLim
