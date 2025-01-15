
from typing import List
from optframe import *
from optframe.protocols import *
from optframe.heuristics import *
from optframe.components import Move
from random import randint

class SolutionPAS(object):
    def __init__(self):
        self.timeslots : List[str] = []
        self.classes : List[str] = []
        self.classrooms : List[str] = []
        self.solution : List[List[List[int]]] = []
    
    def __str__(self):
        return f"SolutionPAS:\ntimeslots={self.timeslots}\nteoric_classes={self.classes}\nteoric_classrooms={self.classrooms}\nsolution={self.solution}"

class PAS(object):
    def __init__(self):
        self.engine = Engine()
        self.timeslots : List[str] = []
        self.classes : List[str] = []
        self.classrooms : List[str] = []

    def load(self, filename : str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            n_timeslots, n_classes, n_classrooms = map(int, lines[0].split())
            for i in range(1, n_timeslots+1):
                self.timeslots.append(lines[i].strip())
            for i in range(n_timeslots+1, n_timeslots+1+n_classes):
                class_ = lines[i].split()
                self.classes.append((class_[0], class_[1], class_[2], int(class_[3])))
            for i in range(n_timeslots+1+n_classes, n_timeslots+1+n_classes+n_classrooms):
                classroom = lines[i].split()
                self.classrooms.append((classroom[0], classroom[1], int(classroom[2])))
            
    def __str__(self):
        return f"PAS:\ntimeslots={self.timeslots}\nclasses={self.classes}\nclassrooms={self.classrooms})"

    @staticmethod
    def generateSolution(problem: 'PAS') -> SolutionPAS:
        sol = SolutionPAS()
        sol.timeslots = problem.timeslots
        sol.classes = [c for c in problem.classes]
        sol.classrooms = [c for c in problem.classrooms]
        sol.solution = [[[randint(0, 1) for _ in range(len(sol.classes))] for _ in range(len(sol.classrooms))] for _ in range(len(sol.timeslots))]
        return sol

    @staticmethod
    def maximize(pPAS: 'PAS', sol: SolutionPAS) -> float:
        eval = 0
        penalty = 20  # Penalização fixa para violações

        # Avaliação de alocações válidas
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classes)):
                for r in range(len(sol.classrooms)):
                    if sol.solution[t][r][c] == 1:                    
                        # Penalizações
                        time, room, capacity = 0, 0, 0
                        if sol.timeslots[t] != sol.classes[c][1]:  # Horário incompatível
                            time = 1
                        if sol.classes[c][2] != sol.classrooms[r][1]:  # Tipo incompatível
                            room = 1
                        if sol.classes[c][3] > sol.classrooms[r][2]:  # Capacidade insuficiente
                            capacity = 1
                        eval -= (5*time + 5*room + 5*capacity)*(time + room + capacity)
                        
                        # Recompensas
                        time, room, capacity = 0, 0, 0
                        if sol.timeslots[t] == sol.classes[c][1]:
                            time = 1
                        if sol.classes[c][2] == sol.classrooms[r][1]:
                            room = 1
                        if sol.classes[c][3] <= sol.classrooms[r][2]:
                            capacity = 1
                        eval += 5*(time + room + capacity)

        # Restrições de unicidade
        # Somente uma classe por sala e por horário
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classrooms)):
                if sum(sol.solution[t][c]) > 1:
                    eval -= penalty
        # Somente uma classe
        for c in range(len(sol.classes)):
            cs = []
            for t in range(len(sol.timeslots)):
                for r in range(len(sol.classrooms)):
                    cs.append(sol.solution[t][r][c])
            result = sum(cs)
            if result > 1:
                eval -= result*penalty
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
        return MoveBitFlip(randint(0, len(pPAS.timeslots)-1), randint(0, len(pPAS.classrooms)-1), randint(0, len(pPAS.classes)-1))

## ================================================
## ================================================

if __name__ == "__main__":
    pPAS = PAS()
    pPAS.load('teste.txt')
    pPAS.engine.setup(pPAS)
    pPAS.engine.add_ns_class(pPAS, NSBitFlip) 
    list_idx = pPAS.engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")
    sa = BasicSimulatedAnnealing(pPAS.engine, 0, 0, list_idx, 0.98, 100, 99999)
    sout = sa.search(15.0)
    print("Best solution: ",   sout.best_s)
    print("Best evaluation: ", sout.best_e)
    sol = sout.best_s
    not_allocated = []
    for c in range(len(sol.classes)):
            cs = []
            for t in range(len(sol.timeslots)):
                for r in range(len(sol.classrooms)):
                    cs.append(sol.solution[t][r][c])
            if sum(cs) < 1:
                not_allocated.append(sol.classes[c])
    print("Not allocated classes: ", not_allocated)
                


# [[[1,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,1],[[0,0,0],[0,0,0],[0,0,0]]]
# [[[1,0,0],[0,0,0],[0,1,0]],[[0,0,0],[0,0,0],[0,0,1],[[0,0,0],[0,0,0],[0,0,0]]]

#[[[[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]]], [[[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]]], [[[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]], [[('Turma1', '07:00', 'T', 35), ('Turma2', '07:00', 'P', 30), ('Turma3', '09:00', 'T', 45)]]]]
# [[[0, 0, 1], [1, 1, 0], [1, 0, 1]], [[1, 1, 0], [0, 0, 0], [1, 0, 0]], [[1, 1, 0], [1, 0, 1], [1, 0, 1]]]