# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings
import random
import time
import exrex
import AppClass


qwe = {'1'}
symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
           'I', 'J', 'K',
           'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '.', '_']


# f  = open("text.txt", 'r')

# a = list()
# a.append('1678')
# print(a[0])

#include <stdio.h>

#print(exrex.getone('[A-Za-z1-9]{,15}'))

print(ord('N'))
print(ord('\n'))
print(ord('o'))


g = open('automatic.txt', 'w')

a = time.perf_counter()

rString = ''

for i in range(1, 1000):                  #количество строк
    rString = exrex.getone('[A-Za-z1-9]{,15}[:]')
    for j in range(1, 7):                  #количество слов в строке
        rString += exrex.getone('[  ]{,5}[A-Za-z1-9]{,3}')
    rString += '\n'
   # print(rString)
    g.write(rString)


'''
for i in range(1, 20):
    for n in range(1, random.randint(1, 5)):
        g.write(random.choice(symbols))
    g.write(':')
    for n in range(1, 7):
        for p in range(1, random.randint(1, 5)):
            g.write(random.choice(symbols))
        g.write(' ')
    g.write('\n')
'''
g.close()

b = time.perf_counter()

test = AppClass.AppClass()

c = time.perf_counter()
test.CheckFile()
d = time.perf_counter()

print("На создание случайного документа потребовалось:", b - a)
print("На работу автомата потребовалось столько:", d - c)







