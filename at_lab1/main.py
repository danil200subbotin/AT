# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings
import random
import time
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

g = open('automatic.txt', 'w')

a = time.perf_counter()

for i in range(1, 20000):
    for n in range(1, random.randint(1, 5)):
        g.write(random.choice(symbols))
    g.write(':')
    for n in range(1, 5):
        for p in range(1, random.randint(1, 5)):
            g.write(random.choice(symbols))
        g.write(' ')
    g.write('\n')

g.close()

b = time.perf_counter()

test = AppClass.AppClass()

c = time.perf_counter()
test.CheckFile()
d = time.perf_counter()

print("На создание случайного документа потребовалось:", b - a)
print("На работу автомата потребовалось столько:", d - c)







