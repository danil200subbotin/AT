
class Node:
    def __init__(self, name="", index=0):
        self.name = name
        self.index = index
        self.groupIndex = 0
        self.parent = None
        self.information = 0
        self.children = list()



class Group:
    def __init__(self, left_index):
        isFull = False
        self.left = left_index
        self.right = 0



class MyRegLib:
    def __init__(self, string):
        self.regString = string
        self.synTree = None
        self.NDA = None
        self.DA = None
        self.shortDA = None
        self.first = 0
        self.last = 0
        self.group = list()
        self.nodes = list()

    def nodificatingAll(self):
        for index, char in enumerate(self.regString):
            self.nodes.append(Node(char, index))

    def closestBrackets(self):
        firstBrac = 1
        secondBrac = len(self.nodes) - 1
        currFBrac = 0
        currSBrac = 0
        priorBracIndicator = True
        isGroupOpen = False
        openedGroupAmount = 0
        for index, char in enumerate(self.nodes):
            #    print(index)
            if (char.name == "(") and (self.nodes[index + 1].name == ":"):
                currFBrac = index + 1
                priorBracIndicator = True
            elif (char.name == "(") and not (self.nodes[index + 1].name == ":") and priorBracIndicator:
                isGroupOpen = True
                openedGroupAmount += 1
            elif char.name == ")":
                if priorBracIndicator and not isGroupOpen:
                    currSBrac = index
                    #               print(currSBrac, currFBrac)
                    #               print(firstBrac, secondBrac)
                    if (currSBrac - currFBrac) < (secondBrac - firstBrac):
                        firstBrac = currFBrac
                        secondBrac = currSBrac
                    priorBracIndicator = False
                elif priorBracIndicator and isGroupOpen:
                    openedGroupAmount -= 1
                    if openedGroupAmount < 1:
                        isGroupOpen = False
    #    print("Самые ближние скобки на позициях:", self.regString[firstBrac], self.regString[secondBrac])
        return firstBrac, secondBrac


    def simplifySubstring(self, first, second):

        self.nodes.pop(second + 1)

        for i in range(first, second + 1):
            print(self.nodes[i].name, end="")
        print()

        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "(":
                    self.group.append(Group(self.nodes[index].index))
                    secondBracketIndex = index + 1
                    while not self.nodes[secondBracketIndex].name == ")":
                        self.nodes[secondBracketIndex].groupIndex = len(self.group)
                        secondBracketIndex += 1
                    self.nodes.pop(secondBracketIndex)
                    self.nodes.pop(index)
                    second -= 2
                    print("after (  $", end="")
                    self.printListOfNodes()

        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "…":
                    print("…")
                    self.nodes[index].children.append(self.nodes[index - 1])
                    self.nodes[index].information = 1
                    self.nodes.pop(index - 1)
                    second -= 1
                    print("after ...  $", end="")
                    self.printListOfNodes()
        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "[":
                    print("[")
                    secondSquareBrac = index + 1
                    while not self.nodes[secondSquareBrac].name == "]":
                        self.nodes[index].children.append(self.nodes[secondSquareBrac])
                        secondSquareBrac += 1
                    for i in range(index + 1, secondSquareBrac + 1):
                        self.nodes.pop(index)
                        second -= 1
                    self.nodes[index].name = "[]"
                    print("after [  $", end="")
                    self.printListOfNodes()
        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "{":
                    print("{")
                    secondFigureBrac = index
                    while not self.nodes[secondFigureBrac].name == "}":
                        secondFigureBrac += 1
                    charNumber = ""
                    for i in range(index + 1, secondFigureBrac):
                        charNumber += self.nodes[i].name
                    print("digit------------>", charNumber)
                    intNumber = int(charNumber)
                    while not self.nodes[index].name == "}":
                       # print("Удаляю вот это", self.nodes[index].name)
                        self.nodes.pop(index)
                        second -= 1
                    self.nodes.pop(index)
                    second -= 1
                    self.nodes.insert(index, Node("{}", index))
                    self.nodes[index].information = intNumber
                    self.nodes[index].children.append(self.nodes[index - 1])
                    self.nodes.pop(index - 1)
                    second -= 1
                    print("after {  $", end="")
                    self.printListOfNodes()

        for index in range(first, second):
            indicator = True
            secondConcanIndex = index + 1
            while indicator:
                if secondConcanIndex <= second:
              #      print("sci =", secondConcanIndex, "s =", second)
                    if not self.nodes[index].name == "|" and not self.nodes[index + 1].name == "|":
                        firstSun = self.nodes[index]
                        secondSun = self.nodes[index + 1]
                        print("Присоединяю", secondSun.name, "к", firstSun.name)
                        self.nodes.pop(index)
                        self.nodes.insert(index, Node("*", self.nodes[index].index))
                        self.nodes[index].children.append(firstSun)
                        self.nodes[index].children.append(secondSun)
                        self.nodes.pop(index + 1)
                        second -= 1
                    else:
                        break
                else:
         #           print("---->" ,"sci =", secondConcanIndex, "s =", second)
                    break
            print("after *  $", end="")
            self.printListOfNodes()

        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "|":
                    print("|")
                    self.nodes[index].name = "||"
                    self.nodes[index].children.append(self.nodes[index - 1])
                    self.nodes[index].children.append(self.nodes[index + 1])
                    self.nodes.pop(index + 1)
                    self.nodes.pop(index - 1)
                    second -= 2
                    print("after |  $", end="")
                    self.printListOfNodes()

        self.nodes.pop(first - 2)
        self.nodes.pop(first - 2)


        print("----------------")
        self.printListOfNodes()
        print("----------------")


    def printListOfNodes(self):
        for i in self.nodes:
            print(i.name, end="")
            print(".", end="")
        print()



    def makeTree(self):
        if self.regString is None:
            print("Incorrect string, please repeat the enter")
            return 1
        self.regString = "(:" + self.regString + ")"
        self.nodificatingAll()
        closest = self.closestBrackets()
        while closest[1] - closest[0] > 1:
            print("Зашел в цикл обработки скобок", closest[1] - closest[0])
            self.simplifySubstring(closest[0] + 1, closest[1] - 1)
            closest = self.closestBrackets()
        print(self.nodes)









            

     #   print("Самые ближние скобки на позициях:", self.regString[result[0]], self.regString[result[1]])





