# Dag 1

# Write a program which will find all such numbers which are divisible by 7 but are not a multiple of 5,
# between 2000 and 3200 (both included).
# The numbers obtained should be printed in a comma-separated sequence on a single line.

# 1
def fun1():
    l = []

    for i in range(2000,3201):
        if (i%7==0) and (i %5 != 0):
            l.append(str(i))

    print(','.join(l)) # Här får man en string med comma i mellan varje tal
    print(l,end=',') # Här får man en list med 'x' och ', ' mellan varje 'x'

# 2
# Write a program which can compute the factorial of a given numbers.
# The results should be printed in a comma-separated sequence on a single line.
# Suppose the following input is supplied to the program:
# 8
# Then, the output should be:
# 40320

def fun2():
    def fact(x):
        if x == 0:
            return 1
        return x * fact(x-1)
    print('skriv ett tal')
    x = int(input())
    print(fact(x))

# 3

# With a given integral number n, write a program to generate a dictionary that contains (i, i*i)
# such that is an integral number between 1 and n (both included). and then the program should print the dictionary.
# Suppose the following input is supplied to the program:
# 8
# Then, the output should be:
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}

def fun3():
    print('Skriv in ett tal ditt as')
    n = int(input())
    d = dict()
    for i in range(1,n+1):
        d[i] = i*i
    print(d)

# 4

# Write a program which accepts a sequence of comma-separated numbers from console and generate a list and a tuple
# which contains every number.
# Suppose the following input is supplied to the program:
# 34,67,55,33,12,98
# Then, the output should be:
# ['34', '67', '55', '33', '12', '98']
# ('34', '67', '55', '33', '12', '98')
def fun4():
    print('Skriv in dina värden här')
    values = str(input())
    l = values.split(",")
    t = tuple(l)
    print (l)
    print (t)

# Heat transfer
import numpy as ny

def Temp(x):
    a = 15
    b = 40
    L = 40/1000

    T = a * (L ** 2 - x ** 2) + b
    return T
def fun5():
    k = 100/3
    a = 15
    x = 40/1000
    tinf = 30
    deltaT = Temp(x)-tinf
    h = -k*2*a/deltaT
    print(h)


if __name__=='__main__':
    fun5()