import sympy
import numpy as np
from sympy import *
import re
# ToDo Неправильная обработка производных при нулевых значениях.
# Если в частной производной отсутствует какой-либо параметр,
# его значение не должно быть утеряно, а должно равняться 0.


print('Нахождение математической модели функции вида: y = √(a0 + a1x + a2x^2 + ... + anx^n)')
print('Введите количество слагаемых: ')
termsNumber = input()
termsNumber = int(termsNumber)
# termsNumber = 3


print('Введите количество тестовых данных: ')
testsNumber = input()
testsNumber = int(testsNumber)
# testsNumber = 3


# print('Чему равно x*?')
# xConverseMethod = input()
# print('Чему равно y*?')
# yConverseMethod = input()


inputData = []
diffNumbers = []
diffs = []
matrixA = []
matrixB = []
matrixC = []
detriminants = []
multipliers = []
I = ''
finalFunction = ''


# Заполнение таблицы входных данных
for i in range(termsNumber):
    if i + 1 == termsNumber:
        inputData.append(['y'])
    else:
        inputData.append(['x' + str(i + 1)])
    for j in range(testsNumber):
        if j == 0:
            print('Введите слагаемые: ', inputData[i][0])
        inputData[i].append(int(input()))
# inputData = [[1, 0, 0], [0, 1, 0], [1, 1, 1]]

for i in range(termsNumber):
    inputData[i].pop(0)


# Возможность дать пользователю выбор приведения выражения к линейному уравнению
# match xConverseMethod:
#     case 'x^j':
#         for i in range(termsNumber - 1):
#             for j in range(testsNumber):
#                 inputData[i][j] = inputData[i][j] ** (i + 1)
#     case 'sqrt(x)':
#         for i in range(testsNumber):
#             inputData[1][j] = math.sqrt(inputData[1][j])
#     case '1/xj':
#         for i in range(termsNumber - 1):
#             for j in range(testsNumber):
#                 inputData[i][j] = 1 / inputData[i][j]
#     case 'xj':
#         for i in range(termsNumber - 1):
#             for j in range(testsNumber):
#                 inputData[i][j] = inputData[i][j]
#
# match yConverseMethod:
#     case 'y':
#         for i in range(testsNumber):
#             inputData[termsNumber - 1][i] = inputData[termsNumber - 1][i]
#     case 'ln(y)':
#         for i in range(testsNumber):
#             inputData[termsNumber - 1][i] = math.log(inputData[termsNumber - 1][i])
#     case '1/y':
#         for i in range(testsNumber):
#             inputData[termsNumber - 1][i] = 1 / inputData[termsNumber - 1][i]
#     case 'y^2':
#         for i in range(testsNumber):
#             inputData[termsNumber - 1][i] = inputData[termsNumber - 1][i] ** 2
#     case 'x/y':
#         for i in range(testsNumber):
#             inputData[termsNumber - 1][i] = inputData[0][i]


#  Преобразование значений
for i in range(termsNumber):
    for j in range(testsNumber):
        if i < termsNumber - 1:
            inputData[i][j] = inputData[i][j] ** (i + 1)
        else:
            inputData[i][j] = inputData[i][j] ** 2


# Заполнение массива параметров
for i in range(termsNumber):
    diffNumbers.append('a' + str(i))


# Приведение входных данных к функции ошибки (I)
for k in range(testsNumber):
    I = I + '('
    for i in range(termsNumber + 1):
        if i != 0:
            if i == termsNumber:
                I = I + ' - ' + str(inputData[i-1][k])
            else:
                I = I + ' + ' + str(inputData[i-1][k]) + '*' + diffNumbers[i]
        else:
            I = I + diffNumbers[i]
    if k == testsNumber - 1:
        I = I + ')**2'
    else:
        I = I + ')**2 + '


# Заполнение массива частных производных по каждому параметру
for i in range(termsNumber):
    a = 'a%s' % i
    diffs.append(diff(I[:], a))
    diffs[i] = str(diffs[i])


# Приведение полученных частных производных к необходимому виду для "вытаскивания" из них нужных значений
def changeDiffs(string):
    string = string.replace(' ', '')
    string = string.split('*', termsNumber)
    length = len(string)
    return string, length


# Поиск позиций "потерявшихся" параметров
def searchLostArgs(string, termsNumber):
    lostCounter = 0
    if len(string) < termsNumber + 1:
        for i in range(len(diffNumbers)):
            for j in range(len(string)):
                if not diffNumbers[i] in string[j]:
                    lostCounter += 1
            if lostCounter >= len(string):
                string.insert(i, '0')
            lostCounter = 0
    return string

# Приведение массива частных производных к матрице
def changeMatrix(string, termsNumber):
    A = []
    A.append(int(string[0]))

    for i in range(termsNumber):
       if i > 0:
           if 'a' in string[i]:
            A.append(int(string[i][2:]))
           else:
            A.append(int(string[i]))

    return A


#  Заполнение матриц А и В
for i in range(termsNumber):
    diffs[i], length = changeDiffs(diffs[i])
    diffs[i] = searchLostArgs(diffs[i], termsNumber)
    matrixA.append(changeMatrix(diffs[i], termsNumber + 1))
    matrixB.append(matrixA[i][termsNumber])
    del matrixA[i][termsNumber]


matrixA = np.array(matrixA)


for i in range(termsNumber):
    matrixB[i] = -matrixB[i]


# Заполнение массива определителей
detriminants.append(int(np.linalg.det(matrixA)))
for i in range(termsNumber):
    matrixC = matrixA
    matrixC = np.array(matrixC)
    for j in range(termsNumber):
        matrixC[j][i] = matrixB[j]
    detriminants.append(int(np.linalg.det(matrixC)))


# Заполнение массива итоговых значений параметров
for i in range(termsNumber + 1):
    if i > 0:
        multipliers.append(detriminants[i]/detriminants[0])


# Округление итоговых значений параметров
for i in range(termsNumber):
    multipliers[i] = round(multipliers[i], 2)


# if yConverseMethod == 'ln(y)':
#     multipliers[0] = math.exp(multipliers[0])


# Составление и вывод итоговой функции (математической модели)
finalFunction = finalFunction + 'y = √('
for i in range(termsNumber):
    if i == 0:
        finalFunction = finalFunction + str(multipliers[i])
    else:
        if multipliers[i] > 0:
            finalFunction = finalFunction + ' + ' + str(multipliers[i]) + '*x^%s' %i
        else:
            finalFunction = finalFunction + ' - ' + str(multipliers[i]) + '*x^%s' %i
finalFunction = finalFunction + ')'


print('Математическая модель заданного выражения:')
print(finalFunction)
