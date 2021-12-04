from matplotlib import pyplot as plt

import relibrary
import networkx as nx


class searchClass:
    def __init__(self, graph, string, regLib=None):
        self.graph = graph
        self.groupsGraphs = list()
        self.sourceString = string
        self.currentString = string
        self.startPos = graph.start
        self.finishPos = graph.finish
        self.currentStatements = list()
        self.currentStatements.append(self.startPos)
        self.defaultCurrentStatements = list()
        self.defaultCurrentStatements.append(self.startPos)
        self.regLib = regLib
        self.graphDrawing = None
        self.drawCheckList = list()

    def search(self):
        self.makeEpsilonClosure()
        while len(self.currentString) > 0:
            self.currentStatements = list(self.defaultCurrentStatements)
            for index, letter in enumerate(self.currentString):
                self.findAndAddGroups()
                self.makeEpsilonClosure()
                self.makeNewStatementsForLetter(letter)
                self.makeEpsilonClosure()
                if self.isFinishHere():
                    print("=======================Найдена подстрока, удовлетворяющая РВ:", "=======================", end=" ")
                    print(self.currentString[:index + 1])
                    found = relibrary.Group(self.currentString[:index + 1])
                    found.processed = self.currentString[:index + 1]
                    self.regLib.groups[0] = found
                    #self.drawGraph()
                    return self.currentString[:index + 1]
                if len(self.currentStatements) == 0:
                    break
            self.currentString = self.currentString[1:]
        print("=======================Подстрока не найдена=======================")
        #self.drawGraph()


    def makeEpsilonClosure(self):
        if self.currentStatements is None:
    #        print("Заставили искать Эпсилон замыкание для пустоты :(")
            return 1
        newStates = list(self.currentStatements)
        for graphState in newStates:
            graphState.colour = 0
        for graphState in newStates:
            if graphState.colour == 1:
                continue
            graphState.colour = 1
            for trans in graphState.transitList:
                if "$" in trans.liters and trans.target.colour == 0:
    #                print("Дополнил замыкание вершинкой")
                    newStates.append(trans.target)
        for graphState in newStates:
            graphState.colour = 0
    #    print("добавил в Z-замыкании:", len(newStates) - len(self.currentStatements), "вершин исходного графа")
        self.currentStatements = newStates
        self.currentStatements = newStates
        return 0

    def makeNewStatementsForLetter(self, letter):
        #print("Ищу переходы для", letter)
        states = self.currentStatements
        newState = list()
        for graphState in states:
            for trans in graphState.transitList:
                if letter in trans.liters:
                    if trans.groupIndex is not None:
                        self.regLib.groups[trans.groupIndex].processed += letter
                    #print("Нашел переход по букве", letter)
                    newState.append(trans.target)
        self.currentStatements = newState

    def isFinishHere(self):
        if self.finishPos in self.currentStatements:
            return True
        else:
            return False

    def findAndAddGroups(self):
        for graphState in self.currentStatements:
            for transIndex, trans in enumerate(graphState.transitList):
                if "()" in trans.liters:
                    self.renderNewSubGraph(graphState, trans, transIndex)


    def renderNewSubGraph(self, graphState, trans, transIndex):
        #print("\n+++создаю подграф для регулярки из группы:", trans.groupIndex)
        #print("+++вот для такой регулярки:", self.regLib.groups[trans.groupIndex].regular)
        newLibGraph = relibrary.MyRegLib(self.regLib.groups[trans.groupIndex].regular, self.regLib.language, trans.groupIndex)
        newLibGraph.compile()
        newGraph = newLibGraph.NFAgraph
        startNode = newGraph.start
        finishNode = newGraph.finish

        #удаляю старый переход по "()" в графе
        graphState.transitList.pop(transIndex)

        #добавляю Эпсилон переход на первую вершину нового графа
        graphState.transitList.append(relibrary.GraphTrans("$", startNode))

        #добавляю Эпсилон переход из последней вершины нового графа в большой граф
        finishNode.transitList.append(relibrary.GraphTrans("$", trans.target))

        #newLibGraph.draw()

        #print("добавил подграф для регулярки", trans.groupIndex)

    def drawGraph(self):
        nfa = self.graph
        self.graphDrawing = nx.DiGraph()
        root = nfa.start
        start = str(id(nfa.start) % 1000)
        finish = str(id(nfa.finish) % 1000)
        self.drawSubGraph(root, start, finish)
        pos2 = nx.planar_layout(self.graphDrawing)
        nx.draw_networkx_nodes(self.graphDrawing, pos2)
        nx.draw_networkx_edges(self.graphDrawing, pos2, arrowsize=15)
        nx.draw_networkx_labels(self.graphDrawing, pos2)
        plt.axis('off')
        plt.show()

    def drawSubGraph(self, node, start, finish):
        #     print("7834t54783065780467320657")
        nodeName = str(id(node) % 1000)
        if nodeName == start:
            nodeName = "start"
        if nodeName == finish:
            nodeName = "finish"
        if not nodeName in self.drawCheckList:
            self.drawCheckList.append(nodeName)
            self.graphDrawing.add_node(nodeName, size=100)
            for trans in node.transitList:
                childName = str(id(trans.target) % 1000)
                if childName == start:
                    childName = "start"
                if childName == finish:
                    childName = "finish"
                self.drawSubGraph(trans.target, start, finish)
                edgeName = "-" + trans.liters[0] + "-" + str(id(trans) % 100)
                #print("НОМЕР ГРУППЫ В ПЕРЕХОДЕ:", trans.groupIndex)
                self.graphDrawing.add_node(edgeName)
                self.graphDrawing.add_edge(nodeName, edgeName)
                self.graphDrawing.add_edge(edgeName, childName)
        #       self.nfaDrawing.add_edge(nodeName, childName, label=trans.liters[0])








#
# class GraphNode:
#     def __init__(self, name="", number=0):
#         self.name = name
# #       self.number = number
#         self.transitList = list()
#         self.colour = 0
#
# class GraphTrans:
#     def __init__(self, liters=None, target=None, groupIndex=None):
#         self.liters = liters
#         self.target = target
#         self.groupIndex = groupIndex