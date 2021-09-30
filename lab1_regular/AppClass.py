import re

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
        for i in self.targets:
            if i.name == self.targetName:
                i.isUsedLikeTarget = False

    def CheckFile(self):
        # filename = input("Введите название файла для анализа")
        skip = 0
        file = open("automatic.txt", 'r')
        for line in file:
            target = re.match(r'\s*[\.\_A-Za-z][\w\.\_]*:', line)
            self.investigatedReq.clear()
            self.buffer = None
            if target:
                self.buffer = target.group().strip()
                self.buffer = self.buffer[:len(self.buffer) - 1]
                if self.isTargetUnique():
                    self.addTarget()
                    line = line[target.end():]
                    testBuffer = re.match(r'\s*[\.\_A-Za-z][\w\.\_]*', line)
                    while testBuffer:
                        self.buffer = testBuffer.group().strip()
                        if self.isReqUnique():
                            line = line[testBuffer.end():]
                            testBuffer = re.match(r'\s*[\.\_A-Za-z][\w\.\_]*', line)
                        else:
                            self.deleteTarget()
                            self.buffer = None
                            testBuffer = None
                            self.investigatedReq.clear()
                    self.addNewReq()
                else:
                    self.deleteTarget()
                    self.buffer = None
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
            self.investigatedReq.append(self.buffer)
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