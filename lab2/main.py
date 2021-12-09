# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import string
import relibrary


# printableSymbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
#                     'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
#                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
#                     'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
#                     'U', 'V', 'W', 'X', 'Y', 'Z', '!', '#', '%', '&', "'", '(', ')', '*',
#                     '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
#                     ']', '^', '_', '`', '{', '}', '~']

printableSymbols = ['0', '1', '2', '3', '4', '5']




subReg1 = relibrary.MyRegLib("1|2", printableSymbols)
subReg1.compile()
subReg1.draw()


subReg1.regexRecovery()
print("Вот что восстановил:", subReg1.regString, "->",  subReg1.recoveredString)





# reg.makeMDFAfromDFA()
# reg.drawMinDFA()


#printableSymbols = string.printable
# chunks = [string.printable[i:i+1] for i in range(0, len(string.printable), 1)]

# reg = relibrary.MyRegLib("(mep)(hi)", printableSymbols)
#
# reg.compile()
#
#
#
# for index, group in enumerate(reg.groups):
#     print(reg.giveStringFromGroup(index))
#
# reg.regexRecovery()
#
# print(reg.reverseRegString)
#
# reg2 = relibrary.MyRegLib(reg.reverseRegString, printableSymbols)
# reg2.compile()
#
# print(reg.reverseRegString)
# print(reg2.reverseRegString)
#
#
#
#
# reg.search("mephihimep")
#
# reg.printSearchingResults()
# #reg.draw()
