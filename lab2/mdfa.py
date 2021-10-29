
import relibrary

class minDFAnode:
    def __init__(self, _nodes=list()):
        self.translist = None
        self.id = 0
        self.nodes = _nodes

class mDFA:
    def __init__(self, DFA):
        self.pi = list()
        self.DFA = DFA
        self.allDFAnodes = DFA.DFAnodes
        self.wasNewSubdLastTime = True

    def makeFirstGroups(self):
        self.pi.append(minDFAnode(list()))
        self.pi[0].id = id(self.pi[0])
        self.pi[0].nodes = list()
        self.pi.append(minDFAnode(list()))
        self.pi[1].id = id(self.pi[1])
        self.pi[1].nodes = list()
        for node in self.allDFAnodes:
            if node.isItFinish:
                node.mDFAid = self.pi[1].id
                self.pi[1].DFAnodes.append(node)
            else:
                node.mDFAid = self.pi[0].id
                print(self.pi[0].nodes)
                self.pi[0].nodes.append(node)

    def nodesTheSame(self, s1, s2):
        sameIndex = True
        sameLiter = False
        targetId = 0
        for trans1 in s1.transitList:
            litera = trans1.liters[0]
            for trans2 in s2.transitList:
                if trans2.liters[0] == litera:
                    sameLiter = True
                    if trans2.target.mDFAid != trans1.target.mDFAid:
                        sameIndex = False
                        return False
            if not sameLiter:
                sameIndex = False
                return False
            sameLiter = False
        return True

    #переменные наименую, как в лекции.
    def makeSubdivision(self, node=minDFAnode):
        self.wasNewSubdLastTime = False
        if node is None:
            print("тут пытаются сделать разделение None вершины mDFA")
            return 1
        pi2 = list()
        #эти лист нужны для разбиений
        newS1 = list()
        newS2 = list()
        newS3 = list()
        for g in self.pi:
            for s1 in g.nodes:
                for s2 in g.nodes:
                    if not self.nodesTheSame(s1, s2):
                        self.wasNewSubdLastTime = True
                        for node in g.nodes:
                            if self.nodesTheSame(node, s1):
                                node.mDFAid = id(newS1)
                                newS1.append(node)
                            else:
                                if self.nodesTheSame(node, s2):
                                    node.mDFAid = id(newS2)
                                    newS2.append(node)
                                else:
                                    node.mDFAid = id(newS3)
                                    newS3.append(node)
                        newNode1 = minDFAnode(newS1)
                        newNode2 = minDFAnode(newS2)
                        newNode3 = minDFAnode(newS3)
                        self.pi.remove(g)
                        self.pi.append(newNode1)
                        self.pi.append(newNode2)
                        self.pi.append(newNode3)

    def makeTransesforMinDFA(self):
        for g in self.pi:
            g.translist = list()
            if len(g.nodes) > 0:
                for trans in g.nodes[0].transitList:
                    for g2 in self.pi:
                        if id(g2) == trans.target.mDFAid:
                            g.translist.append(relibrary.GraphTrans(trans.liters, g2))





"""
class DFAnode:
    def __init__(self, statement=list()):
        self.statement = statement
        self.transitList = list()
        self.isItFinish = False
        self.mDFAid = 0
"""

"""
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
"""

