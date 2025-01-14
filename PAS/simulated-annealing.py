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
        

    def load(self, filename : str):
        return None
        

    def __str__(self):
        return f"PAS:\ntimeslots={self.timeslots}\nclasses={self.classes}\nclassrooms={self.classrooms}\nsolution={self.solution})"

    @staticmethod
    def generateSolution(problem: 'PAS') -> SolutionPAS:
        sol = SolutionPAS()
        return sol

    @staticmethod
    def maximize(pPAS: 'PAS', sol: SolutionPAS) -> float:
        return 0.0

class MoveBitFlip(Move):
    def __init__(self, _k :int):
        self.k = _k

    def apply(self, problemCtx: PAS, sol: SolutionPAS) -> 'MoveBitFlip':
        sol.solution = sol.solution
        return MoveBitFlip(self.k)

    def canBeApplied(self, problemCtx: PAS, sol: SolutionPAS) -> bool:
        return True

    def eq(self, problemCtx: PAS, m2: 'MoveBitFlip') -> bool:
        return self.k == m2.k

    
class NSBitFlip(object):
    @staticmethod
    def randomMove(pPAS: PAS, sol: SolutionPAS) -> MoveBitFlip:
        return MoveBitFlip(randint(0, pPAS.n - 1))

## ================================================
## ================================================

pPAS = PAS()
pPAS.load('knapsack-example.txt')
pPAS.engine.setup(pPAS)
pPAS.engine.add_ns_class(pPAS, NSBitFlip) 
list_idx = pPAS.engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")
sa = BasicSimulatedAnnealing(pPAS.engine, 0, 0, list_idx, 0.98, 100, 99999)
sout = sa.search(10.0)
print("Best solution: ",   sout.best_s)
print("Best evaluation: ", sout.best_e)