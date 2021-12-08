

class RegexTrans:
    def __init__(self, target=None, defaultTrans=None):
        self.isTransDeleted = False
        self.isItExtraTrans = False
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
        self.allRegexesPairs = list()

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
                        regexNode.translist.append(RegexTrans(target=targetRegexNode,
                                                              defaultTrans=dfaTrans.liters[0]))
    def findStartAndFinishNodes(self):
        for node in self.regexNodes:
            if node.isItFinish:
                self.finishNodes.append(node)
            if node.isItStart:
                self.startNodes.append(node)

    def resetRegexes(self):
        for node in self.regexNodes:
            node.isDeleted = False
            print("-------пришло---------->", len(node.translist))
            node.translist[:] = [x for x in node.translist if not x.isItExtraTrans]
            print("--------ушло---------->", len(node.translist))
            for trans in node.translist:
                trans.isTransDeleted = False
                if trans.defaultTrans is not None:
                    trans.regex = trans.defaultTrans

    def deleteExtraNodesForAllPairs(self):
        for startNode in self.startNodes:
            for fiIndex, finishNode in enumerate(self.finishNodes):
                print("ПРОСТО ТЕСТИРУЮ, ЧТО СТАРТ один и тот ЖЕ", id(startNode) % 1000, len(startNode.translist))
                self.resetRegexes()
                print("ПРОСТО ТЕСТИРУЮ, ЧТО СТАРТ один и тот ЖЕ2", id(startNode) % 1000, len(startNode.translist))
                for regexNode in self.regexNodes:
                    if not (regexNode == startNode or regexNode == finishNode):
                        self.deleteNode(regexNode)
                        regexNode.isDeleted = True
                for trans in startNode.translist:
                    if not trans.isTransDeleted:
                        self.addRegexForCurrentStartAndFinishToResult(trans)
                        break


    def deleteNode(self, regexNode):
        print("Удаляю:", id(regexNode) % 1000)
        incomingNodes = list()
        outgoingNodes = list()
        loopTranses = list()
        # сначала определяю те вершины, которые будут слева (картинка с лекции)
        print("количество вершин слева ДО:", len(incomingNodes))
        for node in self.regexNodes:
            for trans in node.translist:
                #ищу вершины, из которых есть переходы в S
                if trans.target == regexNode and node != regexNode and not trans.isTransDeleted:
                    # print("Добавляю incomingNode")
                    incomingNodes.append(node)
        print("количество вершин слева ПОСЛЕ:", len(incomingNodes))

        # теперь определяю те вершины, которые будут справа (картинка с лекции)
        for outgoingTrans in regexNode.translist:  # ищу вершины, в которые есть переходы из S
            if outgoingTrans.target != regexNode and not outgoingTrans.isTransDeleted:
                outgoingNodes.append(outgoingTrans.target)
            else:
                if not outgoingTrans.isTransDeleted:
                    loopTranses.append(outgoingTrans)
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
        isSmthngAppended = False
        if len(regexNode.translist) > 0:
            for leftNode in incomingNodes:
                transToCentral = None
                for index, trans in enumerate(leftNode.translist):
                    if trans.target == regexNode:
                        transToCentral = trans
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
                    for trans in regexNode.translist:
                        if trans.target == rightNode:
                            transFromCentral = trans
                    if transFromCentral is None:
                        print("Критическая ошибка!!! Внимание!!!")

                    #ниже собрана новая ветка для регулярки
                    if straightPath != "":
                        resultRegex = straightPath + "|"
                    resultRegex += "(:"
                    if transToCentral is not None:
                        resultRegex += transToCentral.regex
                    if loopRegular != "":
                        resultRegex += loopRegular
                    resultRegex += transFromCentral.regex
                    resultRegex += ")"
                    newTrans = RegexTrans(target=rightNode)
                    newTrans.regex = resultRegex
                    newTrans.isItExtraTrans = True
                    leftNode.translist.append(newTrans)  #ве
                    isSmthngAppended = True
                if isSmthngAppended:
                    print(id(leftNode) % 1000, "ДЛИИИИИИИИИИИИИНА1 =", len(leftNode.translist))
                    for index, trans in enumerate(leftNode.translist):   # удалил у левой вершины ее пеереход на центрл
                        if trans.target == regexNode:
                            # print("Удаляю вот такую штуку:", len(leftNode.translist))
                            leftNode.translist[index].isTransDeleted = True
                            if len(leftNode.translist) == 0:
                                pass
                            isSmthngAppended = False
                            print("ДЛИИИИИИИИИИИИИНА2 =", len(leftNode.translist))
                            break   # вот эта строчка под вопросом
                else:
                    print("Почему так???")
        else:
            for node in incomingNodes:
                for index, trans in enumerate(node.translist):  # удалил у левой вершины ее пеереход на центрл
                    if trans.target == regexNode:
                        # print("Удаляю вот такую штуку:", len(leftNode.translist))
                        node.translist[index].isTransDeleted = True



                    #вот тут возник затуп, потому что я не понимаю, что делать, если у нас несколько трансов между двумя вершинами (то есть понятно, что там "ИЛИ", но не понятно, возможен ли вообще такай исход у меня)

    def addRegexForCurrentStartAndFinishToResult(self, regex):
        print("Вот такая вышла регуярка для текущих стартовой и конечной вершин", regex.regex)
        print("вот такая текущая регулярка", regex.regex)
        for trans in self.regexNodes[0].translist:
            if trans.target == self.regexNodes[0]:
                print("123")
        if regex.regex not in self.allRegexesPairs:
            if self.resultRegex != "":
                self.resultRegex += "|(:" + regex.regex + ")"
            else:
                self.resultRegex += "(:" + regex.regex + ")"
        self.allRegexesPairs.append(regex.regex)









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


