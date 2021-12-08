from unittest import TestCase, main
import relibrary

printableSymbols2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
                    'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '!', '#', '%', '&', "'", '(', ')', '*',
                    '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
                    ']', '^', '_', '`', '{', '}', '~']


class SearchTest(TestCase):
    def test_one_letter(self):
        a = relibrary.MyRegLib("q", printableSymbols2)
        a.compile()
        a.search("q")
        self.assertEqual("q", a.groups[0].processed)

    def test_simpleConcan(self):
        a = relibrary.MyRegLib("qq", printableSymbols2)
        a.compile()
        a.search("qq")
        self.assertEqual("qq", a.groups[0].processed)

    def test_longConcan(self):
        a = relibrary.MyRegLib("cyuewbcuyber43542354325fwyivbbvfuowbhvf", printableSymbols2)
        a.compile()
        a.search("cyuewbcuyber43542354325fwyivbbvfuowbhvf")
        self.assertEqual("cyuewbcuyber43542354325fwyivbbvfuowbhvf", a.groups[0].processed)

    def test_short_in_the_begin_of_long(self):
        a = relibrary.MyRegLib("cdxydvbwhfrt77t4g267 g64i2bfyr27 fr27 f67r2", printableSymbols2)
        a.compile()
        a.search("cdx")
        self.assertEqual("cdx", a.groups[0].processed)

    def test_short_in_the_middle_of_long(self):
        a = relibrary.MyRegLib("12345", printableSymbols2)
        a.compile()
        a.draw()
        a.search("234")
        self.assertEqual("234", a.groups[0].processed)







if __name__ == '__main__':
    main()


