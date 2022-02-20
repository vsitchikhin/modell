import sympy
from sympy import *
import re



print('Нахождение математической модели функции вида: y = √(a0 + a1x + a2x^2 + ... + anx^n)')
print('Введите количество слагаемых: ')
termsNumber = input()
termsNumber = int(termsNumber)


print('Введите количество тестовых данных: ')
testsNumber = input()
testsNumber = int(testsNumber)


inputData = []
diffNumbers = []
diffs = []
matrix = []
I = ''


for i in range(termsNumber):
    if i + 1 == termsNumber:
        inputData.append(['y'])
    else:
        inputData.append(['x' + str(i + 1)])
    for j in range(testsNumber):
        if j == 0:
            print('Введите слагаемые: ', inputData[i][0])
        inputData[i].append(int(input()))


for i in range(termsNumber):
    inputData[i].pop(0)

# ToDo дать пользователю выбор приведения выражения к линейному уравнению
for i in range(termsNumber):
    for j in range(testsNumber):
        if (i + 1 == termsNumber):
            inputData[i][j] = inputData[i][j] ** 2
        else:
            inputData[i][j] = inputData[i][j] ** (i + 1)


for i in range(termsNumber):
    diffNumbers.append('a' + str(i))


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


for i in range(termsNumber):
    a = 'a%s' % i
    diffs.append(diff(I[:], a))
    diffs[i] = str(diffs[i])
print(diffs)

