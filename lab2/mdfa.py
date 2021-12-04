
import relibrary

class minDFAnode:
    def __init__(self, nodes):
        self.translist = None
        self.id = 0
        self.nodes = nodes
        self.isItStart = False
        self.isItFinish = False
        self.isNodeDeleted = False   #так помечаю те состояния, которые я уже и разделил, но пока боюсь удалять, чтобы ничего не сломать


class mDFA:
    def __init__(self, DFA):
        self.pi = list()
        self.DFA = DFA
        self.start = None
        self.dfaStart = DFA.start
        self.allDFAnodes = DFA.DFAnodes     #тут возможно нужно юзать list()
        self.wasNewSubdLastTime = True


    def isThereStartsAndEnds(self):
        iter = 0
        for dfaNode in self.allDFAnodes:
            if dfaNode.isItFinish:
                iter += 1
                for minDFA in self.pi:
                    if id(minDFA) == dfaNode.mDFAid:
                        minDFA.isItFinish = True
   #             print("реально нашел финиш ДКА, вот такой у него в минДКА хозяин:", dfaNode.mDFAid)
            if dfaNode == self.dfaStart:
                for minDFA in self.pi:
                    if id(minDFA) == dfaNode.mDFAid:
                        minDFA.isItStart = True
                        self.start = minDFA
  #              print("реально нашел старт ДКА, вот такой у него в минДКА хозяин:", dfaNode.mDFAid)
  #      print("вот столько  выходов:", iter)

    def makeFirstGroups(self):
        self.pi.append(minDFAnode(list()))
        self.pi[0].id = id(self.pi[0])
        self.pi[0].nodes = list()
        self.pi.append(minDFAnode(list()))
        self.pi[1].id = id(self.pi[1])
        self.pi[1].nodes = list()
        for node in self.allDFAnodes:
            if node.isItFinish:
                print("Нашел финиш в мин Дка")
                node.mDFAid = self.pi[1].id
                self.pi[1].nodes.append(node)
            else:
                node.mDFAid = self.pi[0].id
                print(self.pi[0].nodes)
                self.pi[0].nodes.append(node)

    def nodesTheSame(self, s1, s2):
        sameIndex = True
        sameLiter = False
        targetId = 0
        for trans1 in s1.transitList:
         #   print(trans1.liters)
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

    def tryToMakeSubdivisionOfNode(self, node):
        self.wasNewSubdLastTime = False
        if node is None:
            print("тут пытаются сделать разделение None вершины mDFA")
            return 1

        nodesSimilarToFirst = list()
        nodesSimilarToSecond = list()
        otherNodes = list()

        firstDiffNode = None
        secondDiffNode = None

        for firstIndex, firstNfaNode in enumerate(node.nodes):
            if self.wasNewSubdLastTime:
                break
            for secondIndex, secondNfaNode in enumerate(node.nodes, start=firstIndex + 1):
                if not self.nodesTheSame(firstNfaNode, secondNfaNode):
        #            print("нашел ноды, по которым теперь буду деленее делать")
                    firstDiffNode = firstNfaNode
                    secondDiffNode = secondNfaNode
                    self.wasNewSubdLastTime = True

            # разбиваю ноды по трем состояниям
        if firstDiffNode is not None:
            for nfaNode in node.nodes:
                if self.nodesTheSame(nfaNode, firstDiffNode):
                    nodesSimilarToFirst.append(nfaNode)
                elif self.nodesTheSame(nfaNode, secondDiffNode):
                    nodesSimilarToSecond.append(nfaNode)
                else:
                    otherNodes.append(nfaNode)
            # создаю по новым состояниям 3 новых нода и добавляю их в pi
            firstNewG = minDFAnode(nodesSimilarToFirst)
            firstNewG.id = id(firstNewG)
            secondNewG = minDFAnode(nodesSimilarToSecond)
            secondNewG.id = id(secondNewG)
            thirdNewG = minDFAnode(otherNodes)
            thirdNewG.id = id(thirdNewG)
            # в каждом из новых нодов элементам показываю индекс вового узла mDFA
            for node in firstNewG.nodes:
                node.mDFAid = firstNewG.id
            for node in secondNewG.nodes:
                node.mDFAid = secondNewG.id
            for node in thirdNewG.nodes:
                node.mDFAid = thirdNewG.id
            # добавляю 3 новых состояния в pi
            self.pi.append(firstNewG)
            self.pi.append(secondNewG)
            self.pi.append(thirdNewG)
            return True  #это значит, что разбиение было, надо бы удалить pi

        return False   #это значит, что разбиения не было, ничего удалять не нужно


    def makeTransesforMinDFA(self):
        for g in self.pi:
            if not g.isNodeDeleted:
                g.translist = list()
                if len(g.nodes) > 0:
                    for trans in g.nodes[0].transitList:
                        for g2 in self.pi:
                            if id(g2) == trans.target.mDFAid:
                                g.translist.append(relibrary.GraphTrans(trans.liters, g2))


    def printNodes(self):
        for node in self.pi:
            print(id(node) % 1000, "del? =", node.isNodeDeleted)

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

