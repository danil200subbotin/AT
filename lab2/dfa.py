

#self.statements будет хранить список списков NFAnodes

class DFAnode:
    def __init__(self, statement=list()):
        self.statement = statement
        self.transitList = list()
        self.isItFinish = False
        self.mDFAid = 0


class DFA:
    def __init__(self):
        self.start = None
        self.finish = None
        self.DFAnodes = list()
        self.isEmptyStateHere = False

    def addStateIfUnique(self, NewNode=None):
        if NewNode.statement is None:
            print("добавил пустое состояние в ДКА")
            if self.isEmptyStateHere:
                for node in self.DFAnodes:
                    if node.statement is None:
                        return node
            else:
                self.isEmptyStateHere = True
                newNode = DFAnode(None)
                self.DFAnodes.append(newNode)
                return newNode
        searchIndicator = True
        currentStateFindIndicator = False
        state = NewNode.statement
        for node in self.DFAnodes:
            oldState = node.statement
            if len(state) != len(oldState):
                continue
            for newT in state:
                for oldT in oldState:
                    if id(newT) == id(oldT):
                        currentStateFindIndicator = True
                searchIndicator = searchIndicator * currentStateFindIndicator
                currentStateFindIndicator = False
                if not searchIndicator:
                    print("сравнил с одним состоянием - не подошло")
                    break
            if searchIndicator:
                print("нашел совпадающее состояние")
                return node
        print("Состояние уникально, добавляю его")
        self.DFAnodes.append(NewNode)
        return NewNode

    def findEpsilonClosure(self, node=None):
        state = node.statement
        print("-------", type(state))
        if state is None:
            print("Заставили искать Эпсилон замыкание для пустоты :(")
            return None
        newState = state
        #T - состояние, t - ребенок состояния (тоже состояние)
        for T in newState:
            if T.colour == 1:
                continue
            T.colour = 1
            for trans in T.transitList:
                if "$" in trans.liters:
                    newState.append(trans.target)
        for T in newState:
            T.colour = 0
        newNode = DFAnode(newState)
        return newNode

    def findAnyLiterClosure(self, liter, node=None):
        state = node.statement
        if state is None:
            print("Заставили искать Эпсилон замыкание для пустоты :(")
            return None
        newState = state
        #T - состояние
        for T in newState:
            if T.colour == 1:
                continue
            T.colour = 1
            for trans in T.transitList:
                if liter in trans.liters:
                    print("нашел переход по вот такой букве:", liter)
                    newState.append(trans.target)
        for T in newState:
            T.colour = 0
        for T in state:
            newState.remove(T)  #удаляю из замыкания изначальные состояния
        newNode = DFAnode(newState)
        return newNode




