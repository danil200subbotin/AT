from unittest import TestCase, main
import relibrary

printableSymbols3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
                    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '!', '#', '%', '&', "'", '(', ')', '*',
                    '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
                    ']', '^', '_', '`', '{', '}', '~']


class SearchTest(TestCase):
    def test_simple_group(self):
        a = relibrary.MyRegLib("(q)", printableSymbols3)
        a.compile()
        a.search("q")
        self.assertEqual("q", a.groups[1].processed)

    def test_simple_group2(self):
        a = relibrary.MyRegLib("(q)(1)", printableSymbols3)
        a.compile()
        a.search("q1")
        self.assertEqual("1", a.groups[2].processed)

    def test_simple_group3(self):
        a = relibrary.MyRegLib("(q)(1)", printableSymbols3)
        a.compile()
        a.search("q1")
        self.assertEqual("q", a.groups[1].processed)

    def test_simple_group4(self):
        a = relibrary.MyRegLib("12(q1)32", printableSymbols3)
        a.compile()
        a.search("12q132")
        self.assertEqual("q1", a.groups[1].processed)

    def test_simple_group5(self):
        a = relibrary.MyRegLib("12(q|1)32", printableSymbols3)
        a.compile()
        a.search("12q32")
        self.assertEqual("q", a.groups[1].processed)

    def test_simple_group6(self):
        a = relibrary.MyRegLib("12(q|1)32", printableSymbols3)
        a.compile()
        a.search("121132")
        self.assertEqual("1", a.groups[1].processed)

    def test_simple_group7(self):
        a = relibrary.MyRegLib("12(1{5})32", printableSymbols3)
        a.compile()
        a.search("1211111132")
        self.assertEqual("11111", a.groups[1].processed)

    def test_simple_group8(self):
        a = relibrary.MyRegLib("12([12])32", printableSymbols3)
        a.compile()
        a.search("12232")
        self.assertEqual("2", a.groups[1].processed)

    def test_simple_group9(self):
        a = relibrary.MyRegLib("12(qwee[1q]2)32", printableSymbols3)
        a.compile()
        a.search("12qwee132")
        self.assertEqual("qwee11", a.groups[1].processed)

    def test_simple_group10(self):
        a = relibrary.MyRegLib("(me)(phi)", printableSymbols3)
        a.compile()
        a.search("mephi")
        self.assertEqual("me", a.groups[1].processed)

    def test_simple_group11(self):
        a = relibrary.MyRegLib("(me)(phi)", printableSymbols3)
        a.compile()
        a.search("mephi")
        self.assertEqual("phi", a.groups[2].processed)

    def test_simple_group12(self):
        a = relibrary.MyRegLib("(me)(p|hi)", printableSymbols3)
        a.compile()
        a.search("mep")
        self.assertEqual("p", a.groups[2].processed)

    def test_simple_group13(self):
        a = relibrary.MyRegLib("(me)(p|hi)", printableSymbols3)
        a.compile()
        a.search("mehi")
        self.assertEqual("hi", a.groups[2].processed)

    def test_simple_group14(self):
        a = relibrary.MyRegLib("(me)(p|hi)", printableSymbols3)
        a.compile()
        a.search("mehi")
        self.assertEqual("hi", a.groups[2].processed)

    def test_simple_group15(self):
        a = relibrary.MyRegLib("(12)(q1)(32)", printableSymbols3)
        a.compile()
        a.search("12q132")
        self.assertEqual("q1", a.groups[2].processed)

    def test_simple_group16(self):
        a = relibrary.MyRegLib("12(q{3}1)32", printableSymbols3)
        a.makeTree()
        a.makeNfaForNode(a.nodes[0])
        a.search("12qqq132")
        self.assertEqual("qqq1", a.groups[1].processed)

    def test_simple_group17(self):
        a = relibrary.MyRegLib("12(q{3})32", printableSymbols3)
        a.compile()
        a.search("12qqq32")
        self.assertEqual("qqq", a.groups[1].processed)

    def test_simple_group18(self):
        a = relibrary.MyRegLib("12([qwe])32", printableSymbols3)
        a.compile()
        a.search("12w32")
        self.assertEqual("w", a.groups[1].processed)

    def test_simple_group19(self):
        a = relibrary.MyRegLib("12(1{3}[qwe])32", printableSymbols3)
        a.compile()
        a.search("12111e132")
        self.assertEqual("111ee", a.groups[1].processed)

    def test_simple_group20(self):
        a = relibrary.MyRegLib("12([qwe])|(:as){3}32", printableSymbols3)
        a.compile()
        a.search("12qweasasas132")
        self.assertEqual("q", a.groups[1].processed)

    def test_simple_group21(self):
        a = relibrary.MyRegLib("12([qwe])|(:(:as){3}(32))", printableSymbols3)
        a.compile()
        a.search("12frewf4asasas32")
        self.assertEqual("32", a.groups[2].processed)


if __name__ == '__main__':
    main()
