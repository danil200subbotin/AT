import re
import ply.lex as lex

class Target:
    def __init__(self, name):
        self.name = name
        self.countOfUses = 0
        self.isUsedLikeTarget = False


class AppClass:

    def __init__(self):
        self.file = None
        self.targetName = ""
        self.targets = list()
        self.buffer = ""
        self.currentSymbol = ''
        self.isFinished = False
        self.investigatedReq = list()

    def addToBuff(self):
        self.buffer = self.buffer + self.currentSymbol

    def clearBuff(self):
        self.buffer = ""

    def isTargetUnique(self):
        for target in self.targets:
            if (self.buffer == target.name) and target.isUsedLikeTarget:
                return False
        return True

    def addTarget(self):
        self.investigatedReq.append(self.buffer)
        self.targetName = self.buffer
        for target in self.targets:
            if (self.buffer == target.name) and not target.isUsedLikeTarget:
                target.isUsedLikeTarget = True
                return 0
        self.targets.append(Target(self.buffer))
        self.targets[len(self.targets) - 1].isUsedLikeTarget = True
        self.targets[len(self.targets) - 1].countOfUses = 0
        self.targets[len(self.targets) - 1].isUsedLikeTarget = True
        return 1

    def deleteTarget(self):
        print("удалил цель")
        for i in self.targets:
            if i.name == self.targetName:
                i.isUsedLikeTarget = False

    def CheckFile(self, allTokens):
        targetIndicator = False
        awaitedForColon = False
        errorIndicator = False
        for line in allTokens:
            if line and not errorIndicator:
                self.buffer = line.value
                self.buffer.strip()
                #   print("------>", self.buffer)
                if line.type == "EOS" and not errorIndicator:
                    self.addNewReq()
                    print("100 normal string", line.value)
                    self.investigatedReq.clear()
                    targetIndicator = False
                if line.type == "EOS" and errorIndicator:
                    errorIndicator = False
                    targetIndicator = False
                if line.type == "TARGET" and not targetIndicator:
                    if self.isTargetUnique():
                        self.addTarget()
                        print("1", line.value)
                        targetIndicator = True
                        awaitedForColon = True
                    else:
                        errorIndicator = True
                        self.deleteTarget()
                        self.buffer = None
                        print("2", line.value)
                        self.investigatedReq.clear()
                if line.type == "COLON":
                    if awaitedForColon:
                        print("3", line.value)
                        awaitedForColon = False
                    else:
                        errorIndicator = True
                        self.deleteTarget()
                        print("4", line.value)
                        self.buffer = None
                        self.investigatedReq.clear()
                if line.type == "SPACE":
                    print("5", line.value)
                    if awaitedForColon:
                        errorIndicator = True
                        awaitedForColon = False
                        print("6", line.value)
                        self.deleteTarget()
                        self.buffer = None
                        self.investigatedReq.clear()
                if line.type == "TARGET" and targetIndicator and self.isReqUnique() and not awaitedForColon:
                    print("7", self.buffer)
                    self.investigatedReq.append(self.buffer)
                elif not awaitedForColon and line.type == "TARGET":
                    errorIndicator = True
                    self.deleteTarget()
                    print("8", line.value)
                    self.buffer = None
                    self.investigatedReq.clear()
            else:
                errorIndicator = False
        self.makeStatistic()

















    def makeStatistic(self):
        print("------------------------------Results------------------------------")
        for target in self.targets:
            if target.isUsedLikeTarget:
                print("Target:", target.name, "using like req:", target.countOfUses, "times")
            else:
                print("Target: (but wasn't described like target)", target.name, "using like req:", target.countOfUses,
                      "times")

    def isReqUnique(self):
        if self.investigatedReq.count(self.buffer) == 0:
            return True
        else:
            return False

    def clearReq(self):
        self.investigatedReq.clear()

    def addNewReq(self):
        if len(self.investigatedReq) > 0:
            self.investigatedReq.pop(0)
            print(self.investigatedReq)
            isReqUnique = True
            for newRec in self.investigatedReq:
                for target in self.targets:
                    if target.name == newRec:
                        target.countOfUses += 1
                        isReqUnique = False
                if isReqUnique:
                    self.targets.append(Target(newRec))
                    self.targets[len(self.targets) - 1].countOfUses += 1
                isReqUnique = True
            return 1

    def whyImHere(self):
        pass