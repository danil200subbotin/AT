from unittest import TestCase, main
import relibrary

printableSymbols4 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
                    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '!', '#', '%', '&', "'", '(', ')', '*',
                    '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
                    ']', '^', '_', '`', '{', '}', '~']


class SearchTest(TestCase):
    def test_simple_recovery(self):
        a = relibrary.MyRegLib("2", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:2)", a.recoveredString)

    def test_simple_recovery2(self):
        a = relibrary.MyRegLib("23", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:23))", a.recoveredString)

    def test_simple_recovery3(self):
        a = relibrary.MyRegLib("23456789456879", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:(:(:(:(:(:(:(:(:(:23)4)5)6)7)8)9)4)5)6)8)7)9))", a.recoveredString)

    def test_simple_recovery4(self):
        a = relibrary.MyRegLib("(:21)|(:35)", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:21))|(:(:35))", a.recoveredString)

    def test_not_simple_recovery(self):
        a = relibrary.MyRegLib("2{2}", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:22))", a.recoveredString)

    def test_not_simple_recovery(self):
        a = relibrary.MyRegLib("2{5}", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:22)2)2)2))", a.recoveredString)

    def test_not_simple_recovery2(self):
        a = relibrary.MyRegLib("2{5}[21]", printableSymbols4)
        a.compile()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:(:22)2)2)2)1))|(:(:(:(:(:(:22)2)2)2)2))", a.recoveredString)

    def test_not_simple_recovery3(self):
        a = relibrary.MyRegLib("23|1…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:$)|(:11…)|(:$1…)|(:(:23))", a.recoveredString)

    def test_not_simple_recovery4(self):
        a = relibrary.MyRegLib("2…|1…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:$)|(:11…)|(:$1…)|(:22…)|(:$1…2…)", a.recoveredString)

    def test_not_simple_recovery5(self):
        a = relibrary.MyRegLib("8|2…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:$)|(:22…)|(:$2…)|(:8)", a.recoveredString)

    def test_not_simple_recovery6(self):
        a = relibrary.MyRegLib("82…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:8)|(:(:82)2…)", a.recoveredString)


    def test_not_simple_recovery7(self):
        a = relibrary.MyRegLib("8{5}2…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:88)8)8)8))|(:(:(:(:(:(:88)8)8)8)2)2…)", a.recoveredString)

    def test_not_simple_recovery8(self):
        a = relibrary.MyRegLib("8{5}2…", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:88)8)8)8))|(:(:(:(:(:(:88)8)8)8)2)2…)", a.recoveredString)

    def test_not_simple_recovery9(self):
        a = relibrary.MyRegLib("8{5}2…[qwe]}", printableSymbols4)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        # a.drawNFA()
        a.makeDfaForNfa()
        # a.drawDFA()
        a.regexRecovery()
        self.assertEqual("(:(:(:(:(:(:(:88)8)8)8)e))|(:(:(:(:(:(:88)8)8)8)2)2…|$e))|(:(:(:(:(:(:(:88)8)8)8)q))|(:(:(:(:(:(:88)8)8)8)2)2…|$q))|(:(:(:(:(:(:(:(:88)8)8)8)e))|(:(:(:(:(:(:88)8)8)8)2)2…|$e)}))|(:(:(:(:(:(:(:(:(:88)8)8)8)e))|(:(:(:(:(:(:88)8)8)8)2)2…|$e)}))|(:(:(:(:(:(:(:88)8)8)8)e))|(:(:(:(:(:(:88)8)8)8)2)2…|$e)}))|(:(:(:(:(:(:(:(:88)8)8)8)q))|(:(:(:(:(:(:88)8)8)8)2)2…|$q)}))|(:(:(:(:(:(:(:(:(:88)8)8)8)q))|(:(:(:(:(:(:88)8)8)8)2)2…|$q)}))|(:(:(:(:(:(:(:88)8)8)8)q))|(:(:(:(:(:(:88)8)8)8)2)2…|$q)}))|(:(:(:(:(:(:(:88)8)8)8)w)}))|(:(:(:(:(:(:(:(:88)8)8)8)2)2…|$w)}))", a.recoveredString)

if __name__ == '__main__':
    main()
