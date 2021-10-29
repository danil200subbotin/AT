# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import string

import relibrary


#создаю массив со всеми печатными символами
printableSymbols = []
allPSymbols = string.printable
for i in allPSymbols:
    printableSymbols.append(i)
print(printableSymbols)


liters = list()
liters.append("3")
if "3" in liters:
    print("нифига себе")


class A:
    def __init__(self):
        self.name = "A"

class B:
    def __init__(self):
        self.name = "B"
        self.a = None

a = A()
b = B()
b.a = a

d = dict()
listik = list()
listik.append(a)
listik.append(b)
if str(id(b)) == str(id(listik[1])):
    print("equal")
print(str(id(b)), "=========??????", id(listik[1]))
print(type(id(b)))
print(id(a), "=========??????", id(listik[1].a))


reg = relibrary.MyRegLib("1|2&322|23", printableSymbols)
reg.makeTree()
reg.makeNfaForNode(reg.nodes[0])
reg.makeDfaForNfa()
reg.makeMDFAfromDFA()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
