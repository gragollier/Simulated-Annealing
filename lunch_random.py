from seabury_lunch import Student, Table, pickAndRemove, calculateDiversity
import random
import numpy as np
import pandas as pd

if __name__ =="__main__":
    tables = np.array([])
    tablesDF = pd.read_csv("teachers.csv")
    tablesName = np.array(tablesDF, dtype=str)
    for i in np.linspace(1, tablesName.shape[0], tablesName.shape[0], dtype=int):
        tables = np.append(tables, [Table(i, tablesName[i - 1])])

    df = pd.read_csv("students.csv")
    names = np.array(df['Name'], dtype=str)
    genders = np.array(df['Gender'], dtype=str)
    grades = np.array(df['Grade'], dtype=int)
    students = np.array([])
    for i in np.linspace(0, names.shape[0] - 1, names.shape[0], dtype=int):
        gender = (genders[i] == "Male")
        students = np.append(students, [Student(names[i], grades[i], gender, tables)])

    for i in np.linspace(1, students.shape[0], students.shape[0], dtype=int):
        randNum = random.randint(0, students.shape[0])

        # students[i - 1].table = (i % tables.shape[0])
        tables[(i - 1) % tables.shape[0]].seats -= 1
        tables[(i - 1) % tables.shape[0]].students = np.append(tables[(i - 1) % tables.shape[0]].students,
                                                           students[randNum - 1])
        students = pickAndRemove(students, randNum - 1)

    average = 0
    for i in tables:
        print()
        print(i.number, i.teacher[0])
        for j in i.students:
            print(j.name)
        average += calculateDiversity(i.students)
    print(average / 27)