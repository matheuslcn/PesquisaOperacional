from typing import List
from random import randint
from numpy import iinfo
import time

class SolutionPAS(object):
    def __init__(self):
        self.timeslots : List[str] = []
        self.classes : List[str] = []
        self.classrooms : List[str] = []
        self.solution : List[List[List[int]]] = []
    
    def fitness(self) -> float:
        eval = 0
        penalty = 20  # Penalização para violações
        reward = 5  # Recompensa para alocações válidas

        # Avaliação de alocações válidas
        for t in range(len(self.timeslots)):
            for c in range(len(self.classes)):
                for r in range(len(self.classrooms)):
                    if self.solution[t][r][c] == 1:                    
                        # Penalizações para violações
                        time, room, capacity = 0, 0, 0
                        if self.timeslots[t] != self.classes[c][1]:  # Horário incompatível
                            time = 1
                        if self.classes[c][2] != self.classrooms[r][1]:  # Tipo incompatível
                            room = 1
                        if self.classes[c][3] > self.classrooms[r][2]:  # Capacidade insuficiente
                            capacity = 1
                        eval -= penalty*((time + room + capacity)**2)
                        
                        # Recompensas
                        time, room, capacity = 0, 0, 0
                        if self.timeslots[t] == self.classes[c][1]:
                            time = 1
                        if self.classes[c][2] == self.classrooms[r][1]:
                            room = 1
                        if self.classes[c][3] <= self.classrooms[r][2]:
                            capacity = 1
                        eval += reward*((time + room + capacity))

        # Restrições de unicidade
        # Somente uma classe por sala e por horário
        for t in range(len(self.timeslots)):
            for c in range(len(self.classrooms)):
                result = sum(self.solution[t][c])
                if result > 1:
                    eval -= penalty*(result**2)
        # Somente uma classe
        for c in range(len(self.classes)):
            cs = []
            for t in range(len(self.timeslots)):
                for r in range(len(self.classrooms)):
                    cs.append(self.solution[t][r][c])
            result = sum(cs)
            if result > 1:
                eval -= penalty*(result**2)
        return eval
    
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
        return f"SolutionPAS:\nSolution={s}\nFitness:{self.fitness()}\nTotal classes allocated={count}\nNot allocated classes={not_allocated_classes}\nInvalid classes={invalid}\nNot allocated classrooms={not_allocated_classrooms}"


class PAS(object):
    def __init__(self):
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
        return f"PAS:\nSolution={s}\nFitness={self.fitness()}\nTotal classes={count}\nNot allocated classes={not_allocated_classes}\nInvalid classes={invalid}\nNot allocated classrooms={not_allocated_classrooms}"


    def generateSolution(self) -> SolutionPAS:
        sol = SolutionPAS()
        sol.timeslots = self.timeslots
        sol.classes = [c for c in self.classes]
        sol.classrooms = [c for c in self.classrooms]
        sol.solution = [[[randint(0, 1) for _ in range(len(sol.classes))] for _ in range(len(sol.classrooms))] for _ in range(len(sol.timeslots))]
        return sol
    
    def crossover(self, sol1: SolutionPAS, sol2: SolutionPAS) -> SolutionPAS:
        sol = SolutionPAS()
        sol.timeslots = self.timeslots
        sol.classes = [c for c in self.classes]
        sol.classrooms = [c for c in self.classrooms]
        sol.solution = [[[sol1.solution[t][r][c] if randint(0, 1) == 1 else sol2.solution[t][r][c] for c in range(len(sol.classes))] for r in range(len(sol.classrooms))] for t in range(len(sol.timeslots))]
        return sol
    
    def mutate(self, sol: SolutionPAS) -> SolutionPAS:
        t_, r_, c_ = randint(0, len(sol.timeslots)-1), randint(0, len(sol.classrooms)-1), randint(0, len(sol.classes)-1)
        sol.solution[t_][r_][c_] = 1 if sol.solution[t_][r_][c_] == 0 else 0
        return sol
    
    def select(self, population: List[SolutionPAS]) -> List[SolutionPAS]:
        return sorted(population, key=lambda x: x.fitness(), reverse=True)
    
    def solve(self, filename : str, n_generations : int, population_size : int, selection_rate: int, mutate_factor: int) -> SolutionPAS:
        self.load(filename)
        population = [self.generateSolution() for _ in range(population_size)]
        generations_without_improvement = 0
        global_best = iinfo(int).min
        for g in range(n_generations):
            print("generation: ", g)
            population = self.select(population)
            best_fitness = population[0].fitness()
            if best_fitness > global_best:
                global_best = best_fitness
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            print("generations without improvement: ", generations_without_improvement)
            if generations_without_improvement > 300:
                return population[0]
            print("best fitness: ", population[0].fitness())
            new_population = []
            for i in range(int(population_size*selection_rate/100)):
                new_population.append(population[i])
            for i in range(len(new_population)):
                s1 = new_population[randint(0, len(new_population)-1)]
                s2 = new_population[randint(0, len(new_population)-1)]
                new_population.append(self.crossover(s1, s2))
            for i in range(len(new_population)):
                while randint(0, 100) < mutate_factor and len(new_population) < population_size:
                    new_population[i] = self.mutate(new_population[i])
            while len(new_population) < population_size:
                new_population.append(self.generateSolution())
            population = new_population
        return population[0]
    
## ================================================
## ================================================

if __name__ == "__main__":
    pPAS = PAS()
    solution_list = []
    arq = input("Enter the file name: ")
    begin = time.time()
    sol = pPAS.solve(f'{arq}.txt', 5000, 100, 10, 20)
    end = time.time()
    solution_list.append((sol, sol.fitness(), end-begin))
    solution_list.sort(key=lambda x: x[1], reverse=True)
    with open(f'outputGenetic-{arq}.txt', 'w') as f:
        f.write(f"{solution_list[0][0]}\n")
        f.write(f"Best evaluation: {solution_list[0][1]}\n")
        f.write(f"Worst evaluation: {solution_list[-1][1]}\n")
        f.write(f"Average evaluation: {sum([x[1] for x in solution_list])/len(solution_list)}\n")
        f.write(f"Average time: {sum([x[2] for x in solution_list])/len(solution_list)}\n")
        f.write(f"Total time: {sum(x[2] for x in solution_list)}\n")
