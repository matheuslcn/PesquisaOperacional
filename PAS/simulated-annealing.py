
from typing import List
from optframe import *
from optframe.protocols import *
from optframe.heuristics import *
from optframe.components import Move
from random import randint
from numpy import dot

class SolutionPAS(object):
    def __init__(self):
        self.timeslots : List[str] = []
        self.teoric_classes : List[str] = []
        self.teoric_classrooms : List[str] = []
        self.pratic_classes : List[str] = []
        self.pratic_classrooms : List[str] = []
        self.solution : List[List[List[int]]] = []
    
    def __str__(self):
        return f"SolutionPAS:\ntimeslots={self.timeslots}\nteoric_classes={self.teoric_classes}\nteoric_classrooms={self.teoric_classrooms}\npratic_classes={self.pratic_classes}\npratic_classrooms={self.pratic_classrooms}\nsolution={self.solution}"

class PAS(object):
    def __init__(self):
        self.engine = Engine()
        self.timeslots : List[str] = []
        self.teoric_classes : List[str] = []
        self.teoric_classrooms : List[str] = []
        self.pratic_classes : List[str] = []
        self.pratic_classrooms : List[str] = []

    def load(self, filename : str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            n_timeslots, n_classes, n_classrooms = map(int, lines[0].split())
            for i in range(1, n_timeslots+1):
                self.timeslots.append(lines[i])
            for i in range(n_timeslots+1, n_timeslots+n_classes+1):
                class_ = lines[i].split()
                self.teoric_classes.append((class_[0], class_[1], int(class_[2]), class_[3]))
            for i in range(n_timeslots+n_classes+1, n_timeslots+n_classes+n_classrooms+1):
                classroom = lines[i].split()
                self.teoric_classrooms.append((classroom[0], classroom[1], int(classroom[2])))
            



    def __str__(self):
        return f"PAS:\ntimeslots={self.timeslots}\nclasses={self.teoric_classes}\nclassrooms={self.teoric_classrooms})"

    @staticmethod
    def generateSolution(problem: 'PAS') -> SolutionPAS:
        sol = SolutionPAS()
        sol.timeslots = problem.timeslots
        sol.teoric_classes = [c for c in problem.teoric_classes]
        sol.teoric_classrooms = [c for c in problem.teoric_classrooms]
        sol.pratic_classes = [c for c in problem.teoric_classes]
        sol.pratic_classrooms = [c for c in problem.teoric_classrooms]
        sol.solution = [[[randint(0, 1) for _ in range(len(sol.teoric_classes))] for _ in range(len(sol.teoric_classrooms))] for _ in range(len(sol.timeslots))]
        return sol

    @staticmethod
    def maximize(pPAS: 'PAS', sol: SolutionPAS) -> float:
        eval = 0
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.teoric_classes)):
                for r in range(len(sol.teoric_classrooms)):
                    eval += sol.solution[t][r][c]

        #TODO: Adicionar restrições
        # Uma classe só pode ser alocada em um único horário
        # Uma classe só pode ser alocada em uma única sala

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