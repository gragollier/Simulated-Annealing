#  Grant Gollier (c)2016

from lunch_opti import *
import numpy as np
import random
import math
import time


def neighbor(seed, tables):
    new_seed = np.array([])
    for i in seed:
        while i < 100:
            i += 1
            shift = np.random.randint(-10, 10)
            new_i = i + shift
            new_i = (new_i % tables.shape[0]) + 1
            if tables[new_i - 1].seats != 0:
                new_seed = np.append(new_seed, new_i)
                tables[new_i - 1].seats -= 1
                break
    return new_seed


students, tables = loadFiles()
solution = initialSoultion(tables, students)
# prettyPrint(score, tables)
# print(neighbor(seed, tables))
# students, tables = loadFiles()
# solution = main(neighbor(seed, tables), tables, students)
# prettyPrint(solution[0], solution[1])


def acceptance_probability(old_cost, new_cost, T):
    # old_cost = abs((((old_cost - 0.9) * 9) * 100) - round(((old_cost - 0.9) * 9) * 100))
    # new_cost = abs((((new_cost - 0.9) * 9) * 100) - round(((new_cost - 0.9) * 9) * 100))
    return math.exp((new_cost - old_cost) / T)


def anneal(solution):
    old_cost = solution[0]
    T = 2
    T_min = 0.01
    alpha = 0.5
    while T > T_min:
        i = 1
        while i <= 100:
            students, tables = loadFiles()
            new_seed = neighbor(solution[2], tables)
            new_cost, new_tables, new_seed = main(new_seed, tables, students)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random.random():
            #if new_cost > old_cost:
                solution = new_cost, new_tables, new_seed
            i += 1
        T = T*alpha
    return solution

start = time.time() # start timer to see how long calculations take
a = anneal(solution) # run annealing over data set
prettyPrint(a[0], a[1]) # print in easy to read format
print(time.time() - start) # print elapsed time

