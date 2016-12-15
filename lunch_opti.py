#  Grant Gollier (c)2016

import numpy as np
import random
import pandas as pd


class Table:
    teacher = str
    seats = 8
    number = int
    students = np.array([])

    def __eq__(self, other):
        if self.number == other:
            return True
        else:
            return False

    def __init__(self, number, teacher):
        self.number = number
        self.teacher = teacher


class Student:
    name = str
    tables = np.array
    grade = int
    gender = bool  # False = Girl True = Male !!!!
    pastTables = np.array([])
    table = int

    def __init__(self, name, grade, gender, tables):
        self.tables = np.array(np.linspace(1, tables.shape[0], tables.shape[0]), dtype=int)
        self.name = name
        self.grade = grade
        self.gender = gender


def pickTable(student, table):
    index = np.full(student.tables.shape, False, bool)
    # inefficient search method below
    for i in np.linspace(0, student.tables.shape[0] - 1, student.tables.shape[0], dtype=int):
        if student.tables[i] == int(table):
            index[i] = True
    table = student.tables[index]
    student.tables = student.tables[~index]
    return student, table


def pickAndRemove(array, indexValue):
    index = np.full(array.shape, False, bool)
    index[indexValue] = True
    array = array[~index]
    return array


def calculateDiversity(array, students):
    numerator = 0
    for i in np.linspace(6, 12, 7, dtype=int):
        total = 0
        for j in array:
            if j.grade == i:
                total += 1
        numerator += total * (total - 1)
    return 1 - (numerator / (students.shape[0] * students.shape[0] - 1))


def place(student, tables):
    for i in tables:
        if i.seats != 0 :
            i.students = np.append(i.students, student)
            i.seats -= 1
            return tables


def generate(students, tables, seed):
    k = 0
    for i in students:
        # j = 0
        # while j < 1000:
        #     j += 1
            randNum = int(seed[k - 1])#random.randint(1, tables.shape[0])
            k += 1
            # if tables[randNum - 1].seats != 0:
            i, a = pickTable(i, randNum)
            i.pastTables = np.append(i.pastTables, [a])
            tables[randNum - 1].seats -= 1
            tables[randNum - 1].students = np.append(tables[randNum - 1].students, i)
            i.table = a
            # break
    return students, tables
# if __name__ == "__main__":


def main(seed, tables, students):


    #seed = np.random.randint(1, tables.shape[0] + 1, 300)

    # try:
    students, tables = generate(students, tables, seed)
    # except IndexError:
    #     average = 0
    #     return average, tables


    # for i in students:
    #     if i.table.shape == 0:
    #         print(i.name, "was unable to find a table, now randomly placing them")
            # place(i, tables)

    average = 0
    total = 0
    toosmall = bool
    for i in tables:
        # print()
        # print(i.number, i.teacher[0])
        total += i.students.shape[0]
        # for j in i.students:
        #     print(j.name)
        average += calculateDiversity(i.students, students)
        toosmall = i.students.shape[0] <= 7
    # print(total)
    if total < students.shape[0]:
        average = 0
    elif toosmall:
        average = (average / (tables.shape[0] + 1)) - 0.5
    else:
        average = average / (tables.shape[0] + 1)
    # print(average)
    return average, tables, seed


        # print(i.number, i.teacher[0])
        # for j in students:
        #     if j.table == i.number:
        #         print(j.name)
        # print()
    # np.save("data.npy", students)


def initialSoultion(tables, students):
    startSeed = np.array([], dtype=int)
    for i in np.linspace(0, students.shape[0] + 1, students.shape[0]):
        while True:
            rand = random.randint(0, tables.shape[0])
            if tables[rand - 1].seats != 0:
                startSeed = np.append(startSeed, rand)
                tables[rand - 1].seats -= 1
                break
    return main(startSeed, tables, students)


def prettyPrint(score, tables):
    total = 0
    for i in tables:
        print()
        print(i.number, i.teacher[0])
        for j in i.students:
            print(j.name)
            total += 1
    print(score, total)


def loadFiles():
    tables = np.array([])
    tablesDF = pd.read_csv("teachers.csv")
    tablesName = np.array(tablesDF, dtype=str)
    for i in np.linspace(1, tablesName.shape[0], tablesName.shape[0], dtype=int):
        tables = np.append(tables, [Table(i, tablesName[i - 1])])

    try:
        students = np.load("data.npy")
    except FileNotFoundError:
        # print("Data file not found generating new one from .csv")
        df = pd.read_csv("students.csv")
        names = np.array(df['Name'], dtype=str)
        genders = np.array(df['Gender'], dtype=str)
        grades = np.array(df['Grade'], dtype=int)
        students = np.array([])
        for i in np.linspace(0, names.shape[0] - 1, names.shape[0], dtype=int):
            gender = (genders[i] == "Male")
            students = np.append(students, [Student(names[i], grades[i], gender, tables)])

    return students, tables

    # for i in students:
    #     j = 0
    #     while j < 1000:
    #         j += 1
    #         randNum = random.randint(1, tables.shape[0])
    #         if tables[randNum - 1].seats != 0:
    #             i, a = pickTable(i, randNum)
    #             i.pastTables = np.append(i.pastTables, [a])
    #             tables[randNum - 1].seats -= 1
    #             tables[randNum - 1].students = np.append(tables[randNum - 1].students, i)
    #             i.table = a
    #             break

# students, tables = loadFiles()
# temp = initialSoultion(tables, students)
# prettyPrint(temp[0], temp[1])