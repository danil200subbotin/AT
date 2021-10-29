import dfa
import mdfa


class Node:
    def __init__(self, name="", index=0, chAmount=0):
        self.name = name
        self.index = index
        self.groupIndex = 0
        self.parent = None
        self.information = 0
        self.children = list()
        self.NFA = None
        for i in range(0, chAmount):
            self.children.append(Node("$"))


class Group:
    def __init__(self, left_index):
        isFull = False
        self.left = left_index
        self.right = 0


class GraphNode:
    def __init__(self, name="", number=0):
        self.name = name
        self.number = number
        self.transitList = list()
        self.colour = 0


class GraphTrans:
    def __init__(self, liters=None, target=None):
        self.liters = liters
        self.target = target
        self.groupID = 0


class NFA:
    def __init__(self, name="", number=0):
        self.name = name
        self.number = number
        self.start = GraphNode("$")
        self.finish = GraphNode("$")


class MyRegLib:
    def __init__(self, string, language):
        self.regString = string
        self.first = 0
        self.last = 0
        self.groups = list()
        self.nodes = list()
        self.NFAgraph = None
        self.DFAgraph = None
        self.mDFA = None
        self.language = language

    def nodificatingAll(self):
        shieldIndicator = False
        for index, char in enumerate(self.regString):
            if char == "\\" and not shieldIndicator:
                shieldIndicator = True
                continue
            if shieldIndicator:
                self.nodes.append(Node("\\" + char, index))
                shieldIndicator = False
                continue
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
                    self.groups.append(Group(self.nodes[index].index))
                    secondBracketIndex = index + 1
                    while not self.nodes[secondBracketIndex].name == ")":
                        self.nodes[secondBracketIndex].groupIndex = len(self.groups)
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
                    self.nodes[index].children.append(Node("$"))

        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "[":
                    print("[")
                    secondSquareBrac = index + 1
                    while not self.nodes[secondSquareBrac].name == "]":
                        self.nodes[index].children.append(self.nodes[secondSquareBrac])
                        secondSquareBrac += 1
                    print("итого внутри", len(self.nodes[index].children), "цифер")
                    for i in range(index + 1, secondSquareBrac + 1):
                        self.nodes.pop(index)
                        second -= 1
                    currentNode = self.nodes[index]
                    children = currentNode.children
                    if len(children) == 1:
                        self.nodes[index] = children[0]
                    else:
                        while len(children) > 1:
                            for i in range(0, 2 - len(currentNode.children)):
                                currentNode.children.append(Node("$"))
                            currentNode.children[0] = children[0]
                            children.pop(0)
                            if len(children) == 1:
                                currentNode.children[1] = children[0]
                                break
                            currentNode.children[1] = Node("|", 0)
                            currentNode = currentNode.children[1]
                    self.nodes[index].name = "[|]"
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
                    self.nodes.insert(index, Node("{&}", index))
                    self.nodes[index].information = intNumber
                    self.nodes[index].children.append(Node("$"))
                    self.nodes[index].children.append(Node("$"))
                    child = self.nodes[index - 1]
                    currentNode = self.nodes[index]
                    if intNumber == 1:
                        currentNode = child
                    while intNumber > 1:
                        for i in range(0, 2 - len(currentNode.children)):
                            currentNode.children.append(Node("$"))
                        currentNode.children[0] = child
                        intNumber -= 1
                        if intNumber == 1:
                            currentNode.children[1] = child
                            break
                        currentNode.children[1] = Node("&")
                        currentNode = currentNode.children[1]

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
                        groupIndex = self.nodes[index].groupIndex
                        self.nodes.pop(index)
                        self.nodes[index].groupIndex = groupIndex
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

        diff = 0
        for index in range(first, second + 1):
            if index - diff <= second:
        #        print("вот на таком элементе я", self.nodes[index - diff].name, "index = ", index - diff, "sec = ", second)
                if self.nodes[index - diff].name == "|":
                    print("|")
                    self.nodes[index - diff].name = "||"
                    self.nodes[index - diff].children.append(self.nodes[index - 1 - diff])
                    self.nodes[index - diff].children.append(self.nodes[index + 1 - diff])
                    self.nodes.pop(index + 1 - diff)
                    self.nodes.pop(index - 1 - diff)
                    diff += 2
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

    def printTreeDependenses(self, node):
        print(node.name, "(", id(node), ")", "have", len(node.children), "children")
        print("\t", end="")
        for j in node.children:
            print(j.name, "(", id(j), ")", "\t", end="")
        print()
        for j in node.children:
            self.printTreeDependenses(j)

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
        self.printTreeDependenses(self.nodes[0])

    def makeNfaForNode(self, node=None):

        for child in node.children:
            if child.NFA is None:
                self.makeNfaForNode(child)

        if node is None:
            print("попытка создать NFA для пустой вершины")
            return 1

        if node.name in {"$"} or len(node.children) == 0:
            print("Обрабатываю совсем пустой узел")
            liters = list()
            liters.append(node.name)
            a = GraphNode("a")
            b = GraphNode("b")
            newTrans = GraphTrans(liters, b)
            a.transitList.append(newTrans)
            newNFA = NFA(node.name)
            newNFA.start = a
            newNFA.finish = b
            node.NFA = newNFA

        if node.name in {"||", "[|]"}:
            print("Обрабатываю или")
            a = GraphNode("a")
            b = GraphNode("b")
            liters = list()
            liters.append("$")
            #создаю 3 необходимых транса (по тетради)
            newTransA = GraphTrans(liters, node.children[0].NFA.start)
            newTransB = GraphTrans(liters, node.children[1].NFA.start)
            newTransC = GraphTrans(liters, b)
            #оборачиваю в новый НКА
            a.transitList.append(newTransA)
            a.transitList.append(newTransB)
            node.children[0].NFA.finish.transitList.append(newTransC)
            node.children[1].NFA.finish.transitList.append(newTransC)
            newNFA = NFA("||")
            newNFA.start = a
            newNFA.finish = b
            node.NFA = newNFA

        if node.name in {"*", "{&}"}:
            print("Обрабатываю И")
            newNFA = NFA("&")
            newNFA.start = node.children[0].NFA.start
            newNFA.finish = node.children[1].NFA.finish
            node.children[0].NFA.finish.transitList = node.children[1].NFA.start.transitList
            node.NFA = newNFA

        if node.name in {"…"}:
            print("Обрабатываю Клини")
            a = GraphNode("a")
            b = GraphNode("b")
            liters = list()
            liters.append("$")
            # создаю 2 необходимых транса (по тетради)
            newTransA = GraphTrans(liters, node.children[0].NFA.start)
            newTransD = GraphTrans(liters, b)
            # оборачиваю в новый НКА
            a.transitList.append(newTransA)
            a.transitList.append(newTransD)
            node.children[0].NFA.finish.transitList.append(newTransA)
            node.children[0].NFA.finish.transitList.append(newTransD)
            newNFA = NFA("…")
            newNFA.start = a
            newNFA.finish = b
            node.NFA = newNFA
        self.NFAgraph = node.NFA
    #    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<NFA готов>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return 0

    def makeDfaForNfa(self):
        if self.NFAgraph is None:
            print("не могу создать NDA, так как нет NFA")
            self.DFAgraph = None
            return 1
        self.DFAgraph = dfa.DFA()
        startPosNFA = self.NFAgraph.start
        finishPosNFA = self.NFAgraph.finish
        startNFAnodes = list()
        startNFAnodes.append(startPosNFA)
        currentState = dfa.DFAnode(startNFAnodes)
        currentState = self.DFAgraph.findEpsilonClosure(currentState)
        self.DFAgraph.start = currentState
        self.DFAgraph.DFAnodes.append(currentState)
        #пошёл обработку по олгоритму с лекции
        for node in self.DFAgraph.DFAnodes:
            for liter in self.language:
                nextNode = self.DFAgraph.findAnyLiterClosure(liter, node)
                nextNode = self.DFAgraph.findEpsilonClosure(nextNode)
                nextNode = self.DFAgraph.addStateIfUnique(nextNode)
                node.transitList.append(GraphTrans(liter, nextNode))
                if finishPosNFA in node.statement:
                    print("Добввляю конечное состояние в DFA")
                    node.isItFinish = True
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DFA готов[", len(self.DFAgraph.DFAnodes), "]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def makeMDFAfromDFA(self):
        print("doing mDFA")
        self.mDFA = mdfa.mDFA(self.DFAgraph)
        self.mDFA.makeFirstGroups()
        while self.mDFA.wasNewSubdLastTime:
            self.mDFA.makeSubdivision()
        self.mDFA.makeTransesforMinDFA()
        print("<<<<<<<<<<----------готов минимизированный ДКА--------------->>>>>>>>>>>>>>>")




"""
class NFAnode:
    def __init__(self, name="", number=0):
        self.name = name
        self.number = number
        self.transitList = list()

class NFAtrans:
    def __init__(self, liters=list(), target=Node("$")):
        self.liters = liters
        self.target = target
        self.groupID = 0

class NFA:
    def __init__(self, name="", number=0):
        self.name = name
        self.number = number
        self.start = Node("$")
        self.finish = Node("$")
"""

     #   print("Самые ближние скобки на позициях:", self.regString[result[0]], self.regString[result[1]])





