import dfa
import mdfa
import networkx as nx
import matplotlib.pyplot as plt
import searching
import RegexRecovery


class Node:
    def __init__(self, name="", index=0, chAmount=0):
        self.name = name
        self.regular = None
        self.reverseRegular = ""
        self.index = index
        self.groupIndex = 0
        self.parent = None
        self.information = 0
        self.children = list()
        self.NFA = None
        for i in range(0, chAmount):
            self.children.append(Node("$"))


class Group:
    def __init__(self, regular=""):
        self.regular = regular
        self.processed = ""
        self.graphStart = None
        self.isFull = False
        self.right = 0


class GraphNode:
    def __init__(self, name="", number=0):
        self.name = name
#       self.number = number
        self.transitList = list()
        self.colour = 0


class GraphTrans:
    def __init__(self, liters=None, target=None, groupIndex=None):
        self.liters = liters
        self.target = target
        self.groupIndex = groupIndex


class NFA:
    def __init__(self, name="", number=0):
        self.regular = None
        self.name = name
        self.number = number
        self.start = GraphNode("$")
        self.finish = GraphNode("$")


class MyRegLib:
    def __init__(self, string, language, groupIndex=None):
        self.groupIndex = groupIndex
        self.regString = string
        self.reverseRegString = ""
        self.first = 0
        self.last = 0
        self.groups = list()
        self.nodes = list()
        self.NFAgraph = None
        self.DFAgraph = None
        self.mDFA = None
        self.language = language
        self.treeDrawing = None
        self.nfaDrawing = None
        self.dfaDrawing = None
        self.mdfaDrawing = None
        self.drawCheckList = list()
        self.dekart = None
        self.groups.append(Group())
        self.recoveredString = None

    def __sub__(self, other):
        #ну вот и настало время написать разность
        self.dekart = dfa.DFA()
        #сначала добавляю вершины
        for indexLeft, nodeLeft in enumerate(self.DFAgraph.DFAnodes):
            for indexRight, nodeRight in enumerate(other.DFAgraph.DFAnodes):
                newNode = dfa.DFAnode(statement=list([indexLeft, indexRight]))
                if nodeLeft.isItFinish and not nodeRight.isItFinish:
                    print("www", "Нашел финиш в разности")
                    newNode.isItFinish = True
                if nodeLeft == self.DFAgraph.start and nodeRight == other.DFAgraph.start:
                    self.dekart.start = newNode
                self.dekart.DFAnodes.append(newNode)
        #теперь добавляю к вернинам грани
        for indexLeft, nodeLeft in enumerate(self.DFAgraph.DFAnodes):
            for indexRight, nodeRight in enumerate(other.DFAgraph.DFAnodes):
                firstSide = self.findNodeforSub(indexLeft, indexRight)
                for letter in self.language:
                    secondSide = self.findSecondSideForSub(nodeLeft, nodeRight, letter, other)
                    newTrans = GraphTrans(liters=list([letter]), target=secondSide)
        return self.dekart

    def findNodeforSub(self, indexLeft, indexRight):
        for node in self.dekart.DFAnodes:
            if node.statement[0] == indexLeft and node.statement[1] == indexRight:
                return node

    def findSecondSideForSub(self, nodeLeft, nodeRight, letter, other):
        firstTarg = None
        secondTarg = None
        for trans in nodeLeft.transitList:
            if letter in trans.liters:
                firstTarg = trans.target
        for trans in nodeRight.transitList:
            if letter in trans.liters:
                secondTarg = trans.target
        firstIndex = -1
        secondIndex = -1
        for indexLeft, node in enumerate(self.DFAgraph.DFAnodes):
            if node == firstTarg:
                firstIndex = indexLeft
        for indexRight, node in enumerate(other.DFAgraph.DFAnodes):
            if node == secondTarg:
                secondIndex = indexRight
        for node in self.dekart.DFAnodes:
            if node.statement[0] == firstIndex and node.statement[1] == secondIndex:
                return node

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

    def makeGroupsAfterNodificating(self):
        isGroupFindedLastTime = True
        while isGroupFindedLastTime:
            isGroupFindedLastTime = False
            for index, node in enumerate(self.nodes):
                newGroupReg = ""
                openBracketsCounter = 0
                if self.nodes[index].name == "(" and self.nodes[index + 1].name != ":":
                    isGroupFindedLastTime = True
                    while not (self.nodes[index + 1].name == ")" and openBracketsCounter == 0):
                        newGroupReg += self.nodes[index + 1].name
                        if self.nodes[index + 1].name == "(":
                            openBracketsCounter += 1
                        if self.nodes[index + 1].name == ")":
                            openBracketsCounter -= 1
                        self.nodes.pop(index + 1)
                    self.nodes.pop(index + 1) #удаляю закрывающуюся скобку
                    self.nodes[index].name = "()"
                    print("Записываю в группу №", len(self.groups), "регулярку", newGroupReg)
                    self.nodes[index].regular = newGroupReg
                    self.nodes[index].groupIndex = len(self.groups)
                    newGroup = Group()
                    newGroup.regular = newGroupReg
                    self.groups.append(newGroup)

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

        # for i in range(first, second + 1):
        #     print(self.nodes[i].name, end="")
        # print()

        for index in range(first, second + 1):
            #print("2index =", first, ",", second)
            if index <= second:
                if self.nodes[index].name == "…":
                    print("…")
                    self.nodes[index].children.append(self.nodes[index - 1])
                    self.nodes[index].children.append(Node("$"))
                    self.nodes[index].information = 1
                    self.nodes.pop(index - 1)
                    second -= 1
                    #print("after ...  $", end="")
                    self.printListOfNodes()
            #print("index =", first, ",", second)

        for index in range(first, second + 1):
            if index <= second:
                if self.nodes[index].name == "[":
                    print("[")
                    secondSquareBrac = index + 1
                    while not self.nodes[secondSquareBrac].name == "]":
                        self.nodes[index].children.append(self.nodes[secondSquareBrac])
                        secondSquareBrac += 1
                    childrenMassiv = self.nodes[index].children
                    for i in range(index + 1, secondSquareBrac + 1):
                        poped = self.nodes.pop(index)
                        second -= 1
                    currentNode = self.nodes[index]
                    children = currentNode.children
                    children.clear()
                    if len(children) == 1:
                        self.nodes[index] = childrenMassiv[0]
                    else:
                        while len(childrenMassiv) > 1:
                            for i in range(0, 2 - len(currentNode.children)):
                                currentNode.children.append(Node("$"))
                            currentNode.children[0] = childrenMassiv[0]
                            childrenMassiv.pop(0)
                            if len(childrenMassiv) == 1:
                                currentNode.children[1] = childrenMassiv[0]
                                break
                            currentNode.children[1] = Node("|")
                            currentNode = currentNode.children[1]
                    self.nodes[index].name = "[|]"
                    #print("after [  $", end="")
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
                        print("Удаляю вот это", self.nodes[index].name)
                        self.nodes.pop(index)
                        second -= 1
                    print("Удаляю вот это", self.nodes[index].name)
                    self.nodes.pop(index)
                    #second -= 1
                    self.nodes.insert(index, Node("{&}", index))
                    self.nodes[index].information = intNumber
                    self.nodes[index].children.append(Node("$"))
                    self.nodes[index].children.append(Node("$"))
                    child = self.nodes[index - 1]
                    currentNode = self.nodes[index]
                    if intNumber == 1:
                        currentNode.children[0] = self.duplicateNode(child)

                    while intNumber > 1:
                     #  print("нужно еще сделать вот столько: ", intNumber, id(currentNode) % 100)
                        for i in range(0, 2 - len(currentNode.children)):
                            currentNode.children.append(Node("$"))
                        currentNode.children[0] = self.duplicateNode(child)
                        intNumber -= 1
                        if intNumber == 1:
                            currentNode.children[1] = self.duplicateNode(child)
                   #        print("ну теперь вот так----", len(currentNode.children))
                            break
                        currentNode.children[1] = Node("&")
                        currentNode = currentNode.children[1]

                    #self.nodes[index].children.append(self.nodes[index - 1])
                    self.nodes.pop(index - 1)
                    second -= 1
                    #print("after {  $", end="")
                    self.printListOfNodes()
                    #print("index = (", first, ",", second, ")")

        for index in range(first, second):
            indicator = True
            secondConcanIndex = index + 1
            while indicator:
                if secondConcanIndex <= second:
              #      print("sci =", secondConcanIndex, "s =", second)
                    if not self.nodes[index].name == "|" and not self.nodes[index + 1].name == "|":
                        firstSun = self.nodes[index]
                        secondSun = self.nodes[index + 1]
                       # print("Присоединяю", secondSun.name, "к", firstSun.name)
                      #  groupIndex = self.nodes[index].groupIndex
                        self.nodes.pop(index)
                      #  self.nodes[index].groupIndex = groupIndex
                        self.nodes.insert(index, Node("*", self.nodes[index].index))
                        self.nodes[index].children.append(firstSun)
                        self.nodes[index].children.append(secondSun)
                        self.nodes.pop(index + 1)
                        second -= 1
                    else:
                        break
                else:
         # print("---->" ,"sci =", secondConcanIndex, "s =", second)
                    break
            #print("after *  $", end="")
            self.printListOfNodes()

        diff = 0
        for index in range(first, second + 1):
            if index - diff <= second:
        # print("вот на таком элементе я", self.nodes[index - diff].name, "index = ", index - diff, "sec = ", second)
                if self.nodes[index - diff].name == "|":
                    print("|")
                    self.nodes[index - diff].name = "||"
                    self.nodes[index - diff].children.append(self.nodes[index - 1 - diff])
                    self.nodes[index - diff].children.append(self.nodes[index + 1 - diff])
                    self.nodes.pop(index + 1 - diff)
                    self.nodes.pop(index - 1 - diff)
                    diff += 2
                    second -= 2
                    #print("after |  $", end="")
                    self.printListOfNodes()
        self.nodes.pop(first - 2)
        self.nodes.pop(first - 2)

        # print("----------------")
        # self.printListOfNodes()
        # print("----------------")


    def duplicateNode(self, node):  #для {} использую
        newNode = Node(node.name)
        for child in node.children:
            newChild = self.duplicateNode(child)
            newNode.children.append(newChild)
        return newNode


    def printListOfNodes(self):
        for i in self.nodes:
            print(i.name, end="")
            print(".", end="")
        print()

    def printTreeDependenses(self, node):
   #     print(node.name, "(", id(node), ")", "have", len(node.children), "children")
        print("\t", end="")
        for j in node.children:
            pass
    #        print(j.name, "(", id(j), ")", "\t", end="")
    #    print()
        for j in node.children:
            self.printTreeDependenses(j)

    def makeTree(self):
        if self.regString is None:
            print("Incorrect string, please repeat the enter")
            return 1
        self.regString = "(:" + self.regString + ")"
        self.nodificatingAll()
        self.makeGroupsAfterNodificating()
        closest = self.closestBrackets()
        while closest[1] - closest[0] > 1:
       #     print("Зашел в цикл обработки скобок", closest[1] - closest[0])
            self.simplifySubstring(closest[0] + 1, closest[1] - 1)
            closest = self.closestBrackets()
        print(self.nodes)
        #self.printTreeDependenses(self.nodes[0])
        self.reverseRegString = self.makeReverseRegex(self.nodes[0])

    def makeReverseRegex(self, node):
        for child in node.children:
            self.makeReverseRegex(child)

        if node is None:
            print("попытка создать NFA для пустой вершины")
            return 1

        if node.name in {"$"} or len(node.children) == 0:
            if node.name == "()":
                node.reverseRegular = "(" + node.regular + ")"
            else:
                node.reverseRegular = node.name

        if node.name in {"||", "[|]", "|"}:
            node.reverseRegular = "(:" + node.children[0].reverseRegular + "|" + node.children[1].reverseRegular + ")"

        if node.name in {"*", "{&}", "&"}:
            node.reverseRegular = "(:" + node.children[1].reverseRegular + node.children[0].reverseRegular + ")"

        if node.name in {"…"}:
            node.reverseRegular = node.children[0].reverseRegular + "…"

        return node.reverseRegular

    #                   NFA


    def makeNfaForNode(self, node=None):

        if node is None:
            print("попытка создать NFA для пустой вершины")
            return 1

        for child in node.children:
            if child.NFA is None:
                self.makeNfaForNode(child)

        if node.name in {"$"} or len(node.children) == 0:
    #        print("Обрабатываю пустой узел или лист")
            liters = list()
            liters.append(node.name)
            a = GraphNode("a")
            b = GraphNode("b")
       #     print("АХТУНГ!!!!", node.groupIndex)
            if self.groupIndex is not None:
                newTrans = GraphTrans(liters, b, self.groupIndex)
            else:
                newTrans = GraphTrans(liters, b, node.groupIndex)
            a.transitList.append(newTrans)
            newNFA = NFA(node.name)
            newNFA.start = a
            newNFA.finish = b
            if node.name == "()":
                newNFA.regular = node.regular
            node.NFA = newNFA

        if node.name in {"||", "[|]", "|"}:
    #        print("Обрабатываю или")
            a = GraphNode("a")
            b = GraphNode("b")
            liters = list()
            liters.append("$")
            #создаю 3 необходимых транса (по тетради)

            if self.groupIndex is not None:
                newTransA = GraphTrans(liters, node.children[0].NFA.start, self.groupIndex)
                newTransB = GraphTrans(liters, node.children[1].NFA.start, self.groupIndex)
                newTransC = GraphTrans(liters, b, self.groupIndex)
            else:
                newTransA = GraphTrans(liters, node.children[0].NFA.start, node.groupIndex)
                newTransB = GraphTrans(liters, node.children[1].NFA.start, node.groupIndex)
                newTransC = GraphTrans(liters, b, node.groupIndex)

            #оборачиваю в новый НКА
            a.transitList.append(newTransA)
            a.transitList.append(newTransB)
            node.children[0].NFA.finish.transitList.append(newTransC)
            node.children[1].NFA.finish.transitList.append(newTransC)
            newNFA = NFA("||")
            newNFA.start = a
            newNFA.finish = b
            node.NFA = newNFA

        if node.name in {"*", "{&}", "&"}:
    #        print("Обрабатываю И")
            newNFA = NFA("&")
            newNFA.start = node.children[0].NFA.start
            newNFA.finish = node.children[1].NFA.finish
            node.children[0].NFA.finish.transitList = node.children[1].NFA.start.transitList
            node.NFA = newNFA


        if node.name in {"…"}:
     #       print("Обрабатываю Клини")
            a = GraphNode("a")
            b = GraphNode("b")
            liters = list()
            liters.append("$")
            # создаю 2 необходимых транса (по тетради)

            if self.groupIndex is not None:
                newTransA = GraphTrans(liters, node.children[0].NFA.start, self.groupIndex)
                newTransD = GraphTrans(liters, b, self.groupIndex)
            else:
                newTransA = GraphTrans(liters, node.children[0].NFA.start, node.groupIndex)
                newTransD = GraphTrans(liters, b, node.groupIndex)

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
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<NFA готов>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return 0

    def makeDfaForNfa(self):
        print("---------------------------------------Начал обработку ДКА---------------------------")
        if self.NFAgraph is None:
            print("не могу создать DFA, так как нет NFA")
            self.DFAgraph = None
            return 1
        self.DFAgraph = dfa.DFA()
        startPosNFA = self.NFAgraph.start
        finishPosNFA = self.NFAgraph.finish
        startNFAnodes = list()
        startNFAnodes.append(startPosNFA)
        currentState = dfa.DFAnode(startNFAnodes)
        currentState = self.DFAgraph.findEpsilonClosure(currentState)
        currentState.isItStart = True
        self.DFAgraph.start = currentState
        self.DFAgraph.DFAnodes.append(currentState)
        #пошёл обработку по алгоритму с лекции
        for index, node in enumerate(self.DFAgraph.DFAnodes):
            if index == 0:
                print("1")
            for liter in self.language:
                nextNode = self.DFAgraph.findAnyLiterClosure(liter, node)
                if nextNode is not None:
                    nextNode = self.DFAgraph.findEpsilonClosure(nextNode)
                    nextNode = self.DFAgraph.addStateIfUnique(nextNode)
                    node.transitList.append(GraphTrans(liter, nextNode))
            if node.statement is not None and finishPosNFA in node.statement:
               # print("Добввляю конечное состояние в DFA")
                        node.isItFinish = True
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DFA готов[", len(self.DFAgraph.DFAnodes), "]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # self.drawNFA()
        # self.drawDFA()
        if self.DFAgraph.emptyState in self.DFAgraph.DFAnodes:
            print("ЧТО_ТО ПОШЛО НЕ ТАК!!!!!! (неверный ДКА)")

    def makeMDFAfromDFA(self):
        print("doing mDFA")
        self.mDFA = mdfa.mDFA(self.DFAgraph)
        self.mDFA.makeFirstGroups()
        wasSubdinLastCicle = True

        while wasSubdinLastCicle:
            wasSubdinLastCicle = False
            for mdfaNode in self.mDFA.pi:
                if not mdfaNode.isNodeDeleted:
                    self.mDFA.tryToMakeSubdivisionOfNode(mdfaNode)
                    if self.mDFA.wasNewSubdLastTime:
                        wasSubdinLastCicle = True
                        mdfaNode.isNodeDeleted = True

        self.mDFA.makeTransesforMinDFA()
        self.mDFA.isThereStartsAndEnds()
        print("<<<<<<<<<<----------готов минимизированный ДКА--------------->>>>>>>>>>>>>>>")


    def drawTree(self):
        print("---------------рисую дерево----------------")
        self.treeDrawing = nx.DiGraph()
        root = self.nodes[0]
        self.addSubtreeToDrawing(root)

        pos = nx.planar_layout(self.treeDrawing, scale=1)

        nx.draw_networkx_nodes(self.treeDrawing, pos)
        nx.draw_networkx_edges(self.treeDrawing, pos,  arrowsize=15)
        nx.draw_networkx_labels(self.treeDrawing, pos)
  #      nx.draw_networkx_edge_labels(self.treeDrawing, pos)
        plt.axis('off')
        plt.show()

    def addSubtreeToDrawing(self, node):

        nodeName = node.name + "!" + str(id(node) % 1000)
        self.treeDrawing.add_node(nodeName)
        for child in node.children:
            childName = child.name + "!" + str(id(child) % 1000)
            self.addSubtreeToDrawing(child)
        #    self.treeDrawing.add_edge(nodeName, childName, label="")
            self.treeDrawing.add_edge(nodeName, childName)

    def drawNFA(self):
        nfa = self.NFAgraph
        self.nfaDrawing = nx.DiGraph()
        root = nfa.start
        start = str(id(nfa.start) % 1000)
        finish = str(id(nfa.finish) % 1000)

        self.drawSubNFA(root, start, finish)

        pos2 = nx.planar_layout(self.nfaDrawing)

        nx.draw_networkx_nodes(self.nfaDrawing, pos2)
        nx.draw_networkx_edges(self.nfaDrawing, pos2, arrowsize=15)
        nx.draw_networkx_labels(self.nfaDrawing, pos2)
   #     nx.draw_networkx_edge_labels(self.nfaDrawing, pos2)
        plt.axis('off')
        plt.show()

    def drawSubNFA(self, node, start, finish):
   #     print("7834t54783065780467320657")
        nodeName = str(id(node) % 1000)
        if nodeName == start:
            nodeName = "start"
        if nodeName == finish:
            nodeName = "finish"
        if not nodeName in self.drawCheckList:
            self.drawCheckList.append(nodeName)
            self.nfaDrawing.add_node(nodeName, size=100)
            for trans in node.transitList:
                childName = str(id(trans.target) % 1000)
                if childName == start:
                    childName = "start"
                if childName == finish:
                    childName = "finish"
                self.drawSubNFA(trans.target, start, finish)
                edgeName = "-" + trans.liters[0] + "-" + str(id(trans) % 100)
                self.nfaDrawing.add_node(edgeName)
                self.nfaDrawing.add_edge(nodeName, edgeName)
                self.nfaDrawing.add_edge(edgeName, childName)
         #       self.nfaDrawing.add_edge(nodeName, childName, label=trans.liters[0])

    def drawDFA(self):
        dfa = self.DFAgraph
        self.dfaDrawing = nx.DiGraph()
        root = dfa.start
        start = str(id(dfa.start) % 1000)
        self.drawCheckList.clear()
        self.drawSubDFA(root, start)
       # pos3 = nx.random_layout(self.dfaDrawing)
        pos3 = nx.planar_layout(self.dfaDrawing)
        nx.draw_networkx_nodes(self.dfaDrawing, pos3)
        nx.draw_networkx_edges(self.dfaDrawing, pos3, arrowsize=15)
        nx.draw_networkx_labels(self.dfaDrawing, pos3)
        nx.draw_networkx_edge_labels(self.dfaDrawing, pos3)
        plt.axis('off')
        plt.show()

    def drawSubDFA(self, node, start):
        nodeName = str(id(node) % 1000)
        zero = str(id(self.DFAgraph.emptyState) % 1000)
        if nodeName == zero:
            nodeName = "zero"
        if nodeName == start:
            nodeName = "start"
        if node.isItFinish:
            nodeName = "Fin" + nodeName
        if nodeName not in self.drawCheckList:
            self.drawCheckList.append(nodeName)
            if nodeName != "zero":
                self.dfaDrawing.add_node(nodeName)
        #    print("Для", id(node) % 1000)
        #    print("переходы:", len(node.transitList))
            for trans in node.transitList:
                childName = str(id(trans.target) % 1000)
                if childName == start:
                    childName = "start"
                if childName == zero:
                    childName = "zero"
                if trans.target.isItFinish:
                    childName = "Fin" + childName
                self.drawSubDFA(trans.target, start)
                if childName != "zero":
                    self.dfaDrawing.add_edge(nodeName, childName, label=trans.liters[0])
                # print("добавил нод дяля", nodeName, "и", childName)

    def drawMinDFA(self):
        self.mDFA.printNodes()
        minDfa = self.mDFA
        self.mdfaDrawing = nx.DiGraph()
        root = minDfa.start
        start = str(id(root) % 1000)
        self.drawCheckList.clear()

        self.drawSubMinDFA(root, start)

        #        pos3 = nx.planar_layout(self.mdfaDrawing, scale=1)
        pos4 = nx.random_layout(self.mdfaDrawing)
        nx.draw_networkx_nodes(self.mdfaDrawing, pos4)
        nx.draw_networkx_edges(self.mdfaDrawing, pos4, arrowsize=15)
        nx.draw_networkx_labels(self.mdfaDrawing, pos4)
        nx.draw_networkx_edge_labels(self.mdfaDrawing, pos4)
        plt.axis('off')
        plt.show()

    def drawSubMinDFA(self, node, start):
        nodeName = str(id(node) % 1000)
        if nodeName == start:
            nodeName = "start"
        if nodeName not in self.drawCheckList:
            self.drawCheckList.append(nodeName)
            self.mdfaDrawing.add_node(nodeName)
            for i in node.translist:
                print("---", i.liters, id(i.target) % 1000)
            for trans in node.translist:
                childName = str(id(trans.target) % 1000)
                if childName == start:
                    childName = "start"
                self.drawSubMinDFA(trans.target, start)
                edgeName = "-" + trans.liters[0] + "-" + str(id(trans) % 100)
                self.mdfaDrawing.add_edge(nodeName, childName, label=trans.liters[0])
                #print("добавил едж", trans.liters[0], "для", nodeName, "и", childName)

    def search(self, string=None):

        #просто добавляю нулевую группу, ЕСЛИ других нет
        if len(self.groups) == 0:
            self.groups.append(Group())

        print("\n\n\n>>>>>>>>>Начинаю поиск<<<<<<<<<   (", string, ")")
        if self.NFAgraph is None:
            print("Досрочное завершение поиска, не найден скомпилированный NFA")
            return 1
        if string is None:
            print("Не могу произвести поиск, нет строки")
            return 1
        search = searching.searchClass(self.NFAgraph, string, self)
        search.search()

    def giveStringFromGroup(self, number):
        if number >= len(self.groups):
            print("Не могу достать эту регулярку, потому что её нет")
            return None
        return self.groups[number].processed


    def compile(self):
        self.makeTree()
        self.makeNfaForNode(self.nodes[0])
        self.makeDfaForNfa()
        #Убрал его только для окончательных тестов (для картинок вернуть)
        #self.makeMDFAfromDFA()


    def draw(self):
        # self.drawTree()
        self.drawNFA()
        self.drawDFA()
        # self.drawMinDFA()


    def regexRecovery(self):
        recovery = RegexRecovery.RegexRecovery(self.DFAgraph)
        self.recoveredString = recovery.makeRegexRecovery()

    def printSearchingResults(self):
        print("Итог поиска регулярки:", self.groups[0].processed)
        print("В группах захвата было:", end=" ")
        for index in range(1, len(self.groups)):
            print(index, ")", self.groups[index].processed, end=" ", sep="")




