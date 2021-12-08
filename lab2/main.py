# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import string
import relibrary


printableSymbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
                    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '!', '#', '%', '&', "'", '(', ')', '*',
                    '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
                    ']', '^', '_', '`', '{', '}', '~']




subReg1 = relibrary.MyRegLib("2|3|34", printableSymbols)
subReg2 = relibrary.MyRegLib("lar1", printableSymbols)
subReg2.compile()
subReg1.compile()
subReg1.draw()

print("Начал восстановление")
subReg1.regexRecovery()
print("закончил восстановление")
print("Вот что восстановил:", subReg1.regString, "->",  subReg1.recoveredString)


a = relibrary.MyRegLib("12345", printableSymbols)
a.compile()
a.draw()
a.search("234")



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
