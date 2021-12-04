# def addStateIfUnique(self, NewNode=None):
#     state = NewNode.statement
#
#     if state is None:
#         print("добавил пустое состояние в ДКА")
#         if self.isEmptyStateHere:
#             for node in self.DFAnodes:
#                 if node.statement is None:
#                     print("вернул  уже имеющееся пустое состояние")
#                     return node
#         else:
#             self.isEmptyStateHere = True
#             newNode = DFAnode(None)
#             self.DFAnodes.append(newNode)
#             return newNode
#
#     searchIndicator = True
#     currentStateFindIndicator = False
#
#     for node in self.DFAnodes:
#         oldState = node.statement
#         if len(state) != len(oldState):
#             continue
#         for newT in state:
#             for oldT in oldState:
#                 if id(newT) == id(oldT):
#                     currentStateFindIndicator = True
#             searchIndicator = searchIndicator * currentStateFindIndicator
#             currentStateFindIndicator = False
#             if not searchIndicator:
#                 print("сравнил с одним состоянием - не подошло")
#                 break
#         if searchIndicator:
#             print("нашел совпадающее состояние")
#             return node
#     print("Состояние уникально, добавляю его")
#     self.DFAnodes.append(NewNode)
#     return NewNode


# def makeSubdivision(self, node=minDFAnode):
#     self.wasNewSubdLastTime = False
#     if node is None:
#         print("тут пытаются сделать разделение None вершины mDFA")
#         return 1
#     pi2 = list()
#     # эти лист нужны для разбиений
#     newS1 = list()
#     newS2 = list()
#     newS3 = list()
#     for g in self.pi:
#         for s1 in g.nodes:
#             for s2 in g.nodes:
#                 if not self.nodesTheSame(s1, s2):
#                     self.wasNewSubdLastTime = True
#                     for node in g.nodes:
#                         print("повторяю самый вложенный цикл", len(g.nodes))
#                         if self.nodesTheSame(node, s1):
#                             node.mDFAid = id(newS1)
#                             newS1.append(node)
#                         else:
#                             if self.nodesTheSame(node, s2):
#                                 node.mDFAid = id(newS2)
#                                 newS2.append(node)
#                             else:
#                                 node.mDFAid = id(newS3)
#                                 newS3.append(node)
#                     newNode1 = minDFAnode(newS1)
#                     newNode2 = minDFAnode(newS2)
#                     newNode3 = minDFAnode(newS3)
#                     # if добавил для прикола
#                     if g in self.pi:
#                         self.pi.remove(g)
#                     self.pi.append(newNode1)
#                     self.pi.append(newNode2)
#                     self.pi.append(newNode3)