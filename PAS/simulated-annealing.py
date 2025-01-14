# OptFrame Python Demo 0-1 Knapsack Problem + Simulated Annealing

from typing import List
from optframe import *
from optframe.protocols import *
from optframe.heuristics import *
from optframe.components import Move
from random import randint
from numpy import dot

class SolutionPAS(object):
    def __init__(self):
        self.timeslots : int = 0
        self.classes : int = 0
        self.classrooms : int = 0
        self.solution : List[List[List[int]]] = []
    
    def __str__(self):
        return f"SolutionPAS:\ntimeslots={self.timeslots}\nclasses={self.classes}\nclassrooms={self.classrooms}\nsolution={self.solution})"

class PAS(object):
    def __init__(self):
        self.engine = Engine()
        self.timeslots : int = 0
        self.classes : int = 0
        self.classrooms : int = 0   

    def load(self, filename : str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.timeslots, self.classes, self.classrooms = map(int, lines[0].split())

    def __str__(self):
        return f"PAS:\ntimeslots={self.timeslots}\nclasses={self.classes}\nclassrooms={self.classrooms}\nsolution={self.solution})"

    @staticmethod
    def generateSolution(problem: 'PAS') -> SolutionPAS:
        sol = SolutionPAS()
        sol.timeslots = problem.timeslots
        sol.classes = problem.classes
        sol.classrooms = problem.classrooms
        sol.solution = [[[randint(0, 1) for _ in range(sol.classes)] for _ in range(sol.classrooms)] for _ in range(sol.timeslots)]
        print(sol.solution)
        return sol

    @staticmethod
    def maximize(pPAS: 'PAS', sol: SolutionPAS) -> float:
        eval = 0
        for t in range(sol.timeslots):
            for c in range(sol.classes):
                for r in range(sol.classrooms):
                    eval += sol.solution[t][r][c]

        #TODO: Adicionar restrições
        return eval

class MoveBitFlip(Move):
    def __init__(self, t_, r_, c_):
        self.t = t_
        self.r = r_
        self.c = c_

    def apply(self, problemCtx: PAS, sol: SolutionPAS) -> 'MoveBitFlip':
        sol.solution[self.t][self.r][self.c] = 1 - sol.solution[self.t][self.r][self.c]
        return MoveBitFlip(self.t, self.r, self.c)

    def canBeApplied(self, problemCtx: PAS, sol: SolutionPAS) -> bool:
        return True

    def eq(self, problemCtx: PAS, m2: 'MoveBitFlip') -> bool:
        return self.t == m2.t and self.r == m2.r and self.c == m2.c

    
class NSBitFlip(object):
    @staticmethod
    def randomMove(pPAS: PAS, sol: SolutionPAS) -> MoveBitFlip:
        return MoveBitFlip(randint(0, pPAS.timeslots-1), randint(0, pPAS.classrooms-1), randint(0, pPAS.classes-1))

## ================================================
## ================================================

pPAS = PAS()
pPAS.load('teste.txt')
pPAS.engine.setup(pPAS)
pPAS.engine.add_ns_class(pPAS, NSBitFlip) 
list_idx = pPAS.engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")
sa = BasicSimulatedAnnealing(pPAS.engine, 0, 0, list_idx, 0.98, 100, 99999)
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)