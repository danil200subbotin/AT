

class RegexTrans:
    def __init__(self, target=None, defaultTrans=None):
        self.target = target
        self.defaultTrans = defaultTrans   #переход из изначального ДКА
        self.regex = ""        #уже переход, построенный на Регулярке

class RegexNode:
    def __init__(self, nodeDfa=None):
        self.isItStart = False
        self.isItFinish = False
        self.isDeleted = False
        self.nodeDfa = nodeDfa
        self.translist = list()
        if self.nodeDfa.transitList is None:
            self.nodeDfa.transitList = list()


class RegexRecovery:
    def __init__(self, dfa):
        self.regexNodes = list()
        self.dfa = dfa
        self.dfaNodes = list(self.dfa.DFAnodes)
        self.startNodes = list()
        self.finishNodes = list()
        self.resultRegex = ""

    def makeRegexRecovery(self):
        self.makeRegexNodes()
        self.findStartAndFinishNodes()
        self.deleteExtraNodesForAllPairs()
        return self.resultRegex

    def makeRegexNodes(self):
        #сначала просто создаем для каждого ДКА нода новый нод
        for node in self.dfaNodes:
            regexNode = RegexNode(node)
            self.regexNodes.append(regexNode)
            regexNode.isItStart = node.isItStart
            regexNode.isItFinish = node.isItFinish
        #создали, теперь бы создать все переходы (кроме переходов в нуль) (поднимаю из ДКА)
        for regexNode in self.regexNodes:
            for dfaTrans in regexNode.nodeDfa.transitList:
                for targetRegexNode in self.regexNodes:
                    if dfaTrans.target == targetRegexNode.nodeDfa:
                        if dfaTrans.target == self.dfa.emptyState:
                            print("плохая теория работает")
                        else:
                            print("хорошая теория сработала", id(dfaTrans.target))
                        regexNode.translist.append(RegexTrans(target=targetRegexNode,
                                                              defaultTrans=dfaTrans.liters[0]))
    def findStartAndFinishNodes(self):
        for node in self.regexNodes:
            if node.isItFinish:
                self.finishNodes.append(node)
            if node.isItStart:
                self.startNodes.append(node)

    def resetRegexes(self):
        defaultTranses = list()
        for node in self.regexNodes:
            node.isDeleted = False
            for trans in node.translist:
                if trans.defaultTrans is not None:
                    trans.regex = trans.defaultTrans
                    defaultTranses.append(trans)
            node.translist = list(defaultTranses)
            defaultTranses.clear()

    def deleteExtraNodesForAllPairs(self):
        for startNode in self.startNodes:
            for finishNode in self.finishNodes:
                self.resetRegexes()
                for regexNode in self.regexNodes:
                    if not (regexNode == startNode or regexNode == finishNode):
                        self.deleteNode(regexNode)
                    self.addRegexForCurrentStartAndFinishToResult(startNode.translist[0])


    def deleteNode(self, regexNode):
        incomingNodes = list()
        outgoingNodes = list()
        loopTranses = list()

        #сначала определяю те вершины, которые будут слева и справва (картинка с лекции)
        for node in self.regexNodes:
            for trans in node.translist:
                #ищу вершины, из которых есть переходы в S
                if trans.target == regexNode and node != regexNode:
                    print("Добавляю incomingNode")
                    incomingNodes.append(node)
                for outcomingTrans in regexNode.translist:
                    # ищу вершины, в которые есть переходы из S
                    if outcomingTrans.target == node:
                        print("Добавляю outgoingNode")
                        outgoingNodes.append(node)
                    #ищу циклические переходы
                    if outcomingTrans.target == regexNode:
                        print("Добавляю loopTrans")
                        loopTranses.append(outcomingTrans)

        print("Определил все смежные вершины")

        #собираю "…" для циклических
        loopRegular = ""
        if len(loopTranses) != 0:
            if len(loopTranses) == 1:
                loopRegular = loopTranses[0].regex + "…"
            if len(loopTranses) > 1:
                loopRegular = "["
                for trans in loopTranses:
                    loopRegular += trans.regex
                loopRegular += "]…"

        #создаю регулярки для каждой пары incomigng-outgoing
        for leftNode in incomingNodes:
            for rightNode in outgoingNodes:
                resultRegex = ""
                straightPath = ""
                #сначала ищу прямые пути между вершинами
                for trans in leftNode.translist:
                    if trans.target == rightNode:
                        if straightPath != "":
                            straightPath += "|"
                        straightPath += trans.regex
                if straightPath != "":
                    straightPath = "(:" + straightPath + ")"
                #теперь соединяю циклическую, прямую и через центральную
                transFromCentral = None
                transToCentral = None
                for index, trans in enumerate(leftNode.translist):
                    if trans.target == regexNode:
                        transToCentral = trans
                        leftNode.translist.pop(index)   #удалил у левой вершины ее пеереход на центрл
                for trans in regexNode.translist:
                    if trans.target == rightNode:
                        transFromCentral = trans
                if transFromCentral is None:
                    print("Критическая ошибка!!! Внимание!!!")

                #ниже собрана новая ветка для регулярки
                if straightPath != "":
                    resultRegex = straightPath + "|"
                resultRegex += "(:"
                resultRegex += transToCentral.regex
                if loopRegular != "":
                    resultRegex += loopRegular
                resultRegex += transFromCentral.regex
                resultRegex += ")"

                newTrans = RegexTrans(target=rightNode)
                newTrans.regex = resultRegex
                leftNode.translist.append(newTrans)  #ве

                    #вот тут возник затуп, потому что я не понимаю, что делать, если у нас несколько трансов между двумя вершинами (то есть понятно, что там "ИЛИ", но не понятно, возможен ли вообще такай исход у меня)

    def addRegexForCurrentStartAndFinishToResult(self, regex):
        print("Вот такая вышла регуярка для текущих стартовой и конечной вершин", regex.regex)
        print("вот такая текущая регулярка", regex.regex)
        if self.resultRegex != "":
            self.resultRegex += "|(:" + regex.regex + ")"
        else:
            self.resultRegex += "(:" + regex.regex + ")"









"""
class minDFAnode:
    def __init__(self, nodes):
        self.translist = None
        self.id = 0
        self.nodes = nodes
        self.isItStart = False
        self.isItFinish = False
        self.isNodeDeleted = False 
"""


