
from typing import List
from optframe import *
from optframe.protocols import *
from optframe.heuristics import *
from optframe.components import Move
from random import randint
import time

class SolutionPAS(object):
    def __init__(self):
        self.timeslots : List[str] = []
        self.classes : List[str] = []
        self.classrooms : List[str] = []
        self.solution : List[List[List[int]]] = []
    
    def __str__(self):
        s = []
        for t in range(len(self.timeslots)):
            for r in range(len(self.classrooms)):
                for c in range(len(self.classes)):
                    if self.solution[t][r][c] == 1:
                        s.append((self.classes[c][0], self.classrooms[r][0], self.timeslots[t]))

        not_allocated_classes = []
        for c in range(len(sol.classes)):
                cs = []
                for t in range(len(sol.timeslots)):
                    for r in range(len(sol.classrooms)):
                        cs.append(sol.solution[t][r][c])
                if sum(cs) < 1:
                    not_allocated_classes.append(sol.classes[c])

        not_allocated_classrooms = []
        for r in range(len(sol.classrooms)):
                for t in range(len(sol.timeslots)):
                    if sum(sol.solution[t][r]) < 1:
                        not_allocated_classrooms.append((sol.classrooms[r][0], sol.timeslots[t]))
        invalid = []
        count = 0
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classes)):
                for r in range(len(sol.classrooms)):
                    if sol.solution[t][r][c] == 1:
                        count += 1
                        if sol.timeslots[t] != sol.classes[c][1] or sol.classes[c][2] != sol.classrooms[r][1] or sol.classes[c][3] > sol.classrooms[r][2]:
                            invalid.append((sol.classes[c], sol.timeslots[t], sol.classrooms[r]))
        return f"PAS:\nSolution={s}\nTotal classes={count}\nNot allocated classes={not_allocated_classes}\nInvalid classes={invalid}\nNot allocated classrooms={not_allocated_classrooms}"

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
        not_allocated = []
        for c in range(len(sol.classes)):
                cs = []
                for t in range(len(sol.timeslots)):
                    for r in range(len(sol.classrooms)):
                        cs.append(sol.solution[t][r][c])
                if sum(cs) < 1:
                    not_allocated.append(sol.classes[c])
        invalid = []
        count = 0
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classes)):
                for r in range(len(sol.classrooms)):
                    if sol.solution[t][r][c] == 1:
                        count += 1
                        if sol.timeslots[t] != sol.classes[c][1] or sol.classes[c][2] != sol.classrooms[r][1] or sol.classes[c][3] > sol.classrooms[r][2]:
                            invalid.append((sol.classes[c], sol.timeslots[t], sol.classrooms[r]))
        return f"PAS:\nSolution={sol}\nTotal classes={count}\nNot allocated classes={not_allocated}\nInvalid classes={invalid}"

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
        penalty = 20  # Penalização para violações
        reward = 5  # Recompensa para alocações válidas

        # Avaliação de alocações válidas
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classes)):
                for r in range(len(sol.classrooms)):
                    if sol.solution[t][r][c] == 1:                    
                        # Penalizações para violações
                        time, room, capacity = 0, 0, 0
                        if sol.timeslots[t] != sol.classes[c][1]:  # Horário incompatível
                            time = 1
                        if sol.classes[c][2] != sol.classrooms[r][1]:  # Tipo incompatível
                            room = 1
                        if sol.classes[c][3] > sol.classrooms[r][2]:  # Capacidade insuficiente
                            capacity = 1
                        eval -= penalty*((time + room + capacity)**2)
                        
                        # Recompensas
                        time, room, capacity = 0, 0, 0
                        if sol.timeslots[t] == sol.classes[c][1]:
                            time = 1
                        if sol.classes[c][2] == sol.classrooms[r][1]:
                            room = 1
                        if sol.classes[c][3] <= sol.classrooms[r][2]:
                            capacity = 1
                        eval += reward*((time + room + capacity))

        # Restrições de unicidade
        # Somente uma classe por sala e por horário
        for t in range(len(sol.timeslots)):
            for c in range(len(sol.classrooms)):
                result = sum(sol.solution[t][c])
                if result > 1:
                    eval -= penalty*(result**2)
        # Somente uma classe
        for c in range(len(sol.classes)):
            cs = []
            for t in range(len(sol.timeslots)):
                for r in range(len(sol.classrooms)):
                    cs.append(sol.solution[t][r][c])
            result = sum(cs)
            if result > 1:
                eval -= penalty*(result**2)
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
    arq = input("Enter the file name: ")
    pPAS.load(f"{arq}.txt")
    pPAS.engine.setup(pPAS)
    pPAS.engine.add_ns_class(pPAS, NSBitFlip) 
    list_idx = pPAS.engine.create_component_list("[ OptFrame:NS 0 ]", "OptFrame:NS[]")
    solution_list = []
    for _ in range(10):
        begin = time.time()
        sa = BasicSimulatedAnnealing(pPAS.engine, 0, 0, list_idx, 0.5, 500, 9999999)
        sout = sa.search(60)
        sol = sout.best_s
        end = time.time()
        solution_list.append((sout, sout.best_e, end-begin))


    solution_list.sort(key=lambda x: x[1], reverse=True)

    with open(f'outputSimulatedAnnealing-{arq}.txt', 'w') as f:
        f.write(f"{solution_list[0][0].best_s}\n")
        f.write(f"Best evaluation: {solution_list[0][1]}\n")
        f.write(f"Worst evaluation: {solution_list[-1][1]}\n")
        f.write(f"Average evaluation: {sum([x[1] for x in solution_list])/len(solution_list)}\n")
        f.write(f"Average time: {sum([x[2] for x in solution_list])/len(solution_list)}\n")
        f.write(f"Total time: {sum(x[2] for x in solution_list)}\n")        