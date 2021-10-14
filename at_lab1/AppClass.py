import AppClass_sm

colon = {':'}

digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
           'I', 'J', 'K',
           'L', 'M', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}

separators = {'.', '_'}



class Target:
    def __init__(self, name):
        self.name = name
        self.countOfUses = 0
        self.isUsedLikeTarget = False


class AppClass:

    def __init__(self):
        self._fsm = AppClass_sm.AppClass_sm(self)
        self.file = None
        self.targetName = ""
        self.targets = list()
        self.buffer = ""
        self.currentSymbol = ''
        self.isFinished = False
        self.investigatedReq = list()
        self.stringNumber = 1
        self.isStringCorrect = False

    def stringIsNotCorrect(self):
        self.isStringCorrect = False
        print("String", self.stringNumber, "is NOT correct!")
        self.stringNumber += 1

    def stringIsCorrect(self):
        self.isStringCorrect = True
        print("String", self.stringNumber, "is correct!")
        self.stringNumber += 1

    def addToBuff(self):
        self.buffer = self.buffer + self.currentSymbol

    def clearBuff(self):
        self.buffer = ''

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
  #      print(self.targetName)
  #      print(self.targets[0].name, '<<<<<-----')
        for i in self.targets:
            if i.name == self.targetName:
                i.isUsedLikeTarget = False

    def CheckFile(self):
        # filename = input("Введите название файла для анализа")
        f = open("automatic.txt", 'r')
        self._fsm.enterStartState()
        self.currentSymbol = f.read(1)
        while self.currentSymbol != '':
            if self.currentSymbol in letters:
                self._fsm.Lett()
            elif self.currentSymbol in separators:
                self._fsm.Sep()
            elif self.currentSymbol in digits:
                self._fsm.Dig()
            elif self.currentSymbol in colon:
                self._fsm.Colon()
            elif self.currentSymbol == ' ':
                self._fsm.Space()
            elif self.currentSymbol == '\n':
                self._fsm.EOS()
            else:
                self._fsm.Unknown()
            #    print(self.currentSymbol)
            self.currentSymbol = f.read(1)
        self._fsm.EOF()
        return True

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
     #   print(self.investigatedReq)
        if len(self.investigatedReq) > 0:
            self.investigatedReq.pop(0)
   #         print('<<<<<<<<<<<<<<<<<<<<vbyieowg y8vobfiwo bv>>>>>>>>>>>>>>>>>>>>', self.investigatedReq)
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
