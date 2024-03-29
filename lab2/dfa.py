
# self.statements будет хранить список списков NFAnodes
import relibrary

class DFAnode:
    def __init__(self, statement=list()):
        self.statement = statement
        self.transitList = list()
        self.isItFinish = False
        self.isItStart = False
        self.isHereRegular = False
        self.mDFAid = -1

"""class mDFA:
    def __init__(self, DFA):
        self.pi = list()
        self.DFA = DFA
        self.start = None
        self.dfaStart = DFA.start
        self.allDFAnodes = DFA.DFAnodes     #тут возможно нужно юзать list()
        self.wasNewSubdLastTime = True"""


class DFA:
    def __init__(self):
        self.start = None
        self.DFAnodes = list()
        self.isEmptyStateHere = True
        self.emptyState = DFAnode(None)
        self.finishNodesForSub = list()
        self.indexForSub = -1


    #    print("вот координата нуля:", id(self.emptyState) % 1000)

    def addStateIfUnique(self, NewNode=None):
        state = NewNode.statement
        if state is None:
            return None

        isDiffWithCurrState = False

        for node in self.DFAnodes:
            oldState = node.statement
            if len(state) != len(oldState):
      #          print("длины не равны, даже сравнивать не буду")
                continue
            for newT in state:
                if newT not in oldState:
                    isDiffWithCurrState = True
                    break
            if not isDiffWithCurrState:
     #           print("нашел такое же состояние")
                return node
     #   print("!!!!!!!!Состояние уникально, добавляю его")
        self.DFAnodes.append(NewNode)
        print("Ну вот здесь добавил нод в ДКА")
      #  print("Вот такое это состояние:")
      #   for iterator in NewNode.statement:
      #       print(iterator.name)
        return NewNode

    def findEpsilonClosure(self, node=None):
        if node.statement is None:
            return None
        state = node.statement
        newState = list(state)
        # T - состояние(исходного НКА), t - ребенок состояния (тоже состояние)
        for T in newState:
            if T.colour == 1:
                continue
            T.colour = 1
            for trans in T.transitList:
                if "$" in trans.liters and trans.target.colour == 0:
       #             print("Дополнил замыкание вершинкой")
                    newState.append(trans.target)
        newNode = DFAnode(newState)
        for T in newState:
            T.colour = 0
     #   print("добавил в Z-замыкании:", len(newState) - len(state), "вершин исходного НКА")
        return newNode

    def findAnyLiterClosure(self, liter, node=None):
        state = node.statement
        if state is None:
            return None
        newState = list(state)
        finalNewState = list()
        for T in newState:  # T - состояние (исходного НКА)
            if T.colour == 1:
                continue
            T.colour = 1
            for trans in T.transitList:
                if liter in trans.liters:
                    if trans.target in newState:
                        node.transitList.append(relibrary.GraphTrans(liter, node))
                    else:
                        finalNewState.append(trans.target)
        for T in newState:
            T.colour = 0

        if len(finalNewState) == 0:
            return None
        else:
            return DFAnode(finalNewState)

