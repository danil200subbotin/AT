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
        a.search("dxy")
        self.assertEqual("", a.groups[0].processed)

    def test_short_in_the_middle_of_long(self):
        a = relibrary.MyRegLib("12345", printableSymbols2)
        a.compile()
        a.search("23")
        self.assertEqual("", a.groups[0].processed)


    def test_short_in_the_end_of_long(self):
        a = relibrary.MyRegLib("cdxydvbwhfrt77t4g267 g64i2bfyr27 fr27 f67r2", printableSymbols2)
        a.compile()
        a.search("r27 fr27 f67r2")
        self.assertEqual("", a.groups[0].processed)

    def test_very_long_in_the_end_of_very_long(self):
        a = relibrary.MyRegLib("cdxydvbwhfrt77t4g2"
                               "67 gbhukvkviygyivtI VIVTYI VYIVCG"
                               "YIEVGYigyivi rgeiw vbcdgvi gfiwncjiobfe ui"
                               "64i2bfyr27 hic bdowbou c"
                               "cbdhuow bchuohdo"
                               "fr27 f67r2", printableSymbols2)
        a.compile()
        a.search("cdxydvbwhfrt77t4g2"
                               "67 gbhukvkviygyivtI VIVTYI VYIVCG"
                               "YIEVGYigyivi rgeiw vbcdgvi gfiwncjiobfe ui"
                               "64i2bfyr27 hic bdowbou c"
                               "cbdhuow bchuohdo"
                               "fr27 f67r2")
        self.assertEqual("cdxydvbwhfrt77t4g2"
                               "67 gbhukvkviygyivtI VIVTYI VYIVCG"
                               "YIEVGYigyivi rgeiw vbcdgvi gfiwncjiobfe ui"
                               "64i2bfyr27 hic bdowbou c"
                               "cbdhuow bchuohdo"
                               "fr27 f67r2", a.groups[0].processed)

    def test_s1mple_or1(self):
        a = relibrary.MyRegLib("1|2", printableSymbols2)
        a.compile()
        a.search("1")
        self.assertEqual("1", a.groups[0].processed)

    def test_s1mple_or2(self):
        a = relibrary.MyRegLib("1|2", printableSymbols2)
        a.compile()
        a.search("2")
        self.assertEqual("2", a.groups[0].processed)

    def test_s1mple_or_and(self):
        a = relibrary.MyRegLib("12|34", printableSymbols2)
        a.compile()
        a.search("12")
        self.assertEqual("12", a.groups[0].processed)

    def test_s1mple_or_and_or(self):
        a = relibrary.MyRegLib("12|34", printableSymbols2)
        a.compile()
        a.search("34")
        self.assertEqual("34", a.groups[0].processed)

    def test_not_s1mple_or_and_or1(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("12")
        self.assertEqual("12", a.groups[0].processed)

    def test_not_s1mple_or_and_or2(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("34")
        self.assertEqual("34", a.groups[0].processed)

    def test_not_s1mple_or_and_or3(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("5677")
        self.assertEqual("5677", a.groups[0].processed)

    def test_not_s1mple_or_and_or4(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("e2524")
        self.assertEqual("e2524", a.groups[0].processed)

    def test_not_s1mple_or_and_or5(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("34577")
        self.assertEqual("34", a.groups[0].processed)

    def test_not_s1mple_or_and_or6(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("cfre")
        self.assertEqual("cfre", a.groups[0].processed)

    def test_not_s1mple_or_and_or7(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|34577|cfre|rvre", printableSymbols2)
        a.compile()
        a.search("rvre")
        self.assertEqual("rvre", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority1(self):
        a = relibrary.MyRegLib("12|34|5677|e2524|(:34577|cfre|rvre)", printableSymbols2)
        a.compile()
        a.search("34577")
        self.assertEqual("34", a.groups[0].processed)


    def test_not_s1mple_or_and_or_with_priority2(self):
        a = relibrary.MyRegLib("(:12|34|5677|e2524)(:34577|cfre|rvre)", printableSymbols2)
        a.compile()
        a.search("345")
        self.assertEqual("", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority3(self):
        a = relibrary.MyRegLib("(:12)(:34577)", printableSymbols2)
        a.compile()
        a.search("1234577")
        self.assertEqual("1234577", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority4(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("1234577")
        self.assertEqual("12345", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority4(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("1277")
        self.assertEqual("1277", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority5(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("345")
        self.assertEqual("", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority6(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("12")
        self.assertEqual("", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority7(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("12345")
        self.assertEqual("12345", a.groups[0].processed)

    def test_not_s1mple_or_and_or_with_priority8(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("1277")
        self.assertEqual("1277", a.groups[0].processed)

    def test_s1mple_in_the_middle(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("ncjifpnu wip1277uoi fehwo")
        self.assertEqual("1277", a.groups[0].processed)

    def test_s1mple_in_the_end(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("ncjifpnu wipuoi fehwo1277")
        self.assertEqual("1277", a.groups[0].processed)

    def test_s1mple_in_the_end2(self):
        a = relibrary.MyRegLib("(:(:(:12)))(:345|77)", printableSymbols2)
        a.compile()
        a.search("ncjifpnu wipuoi fehwo1277")
        self.assertEqual("1277", a.groups[0].processed)

    def test_s1mple_in_the_middle(self):
        a = relibrary.MyRegLib("(:12)(:345|77)", printableSymbols2)
        a.compile()
        a.search("ncjifpnu wip1277uoi fehwo")
        self.assertEqual("1277", a.groups[0].processed)

    def test_repeating(self):
        a = relibrary.MyRegLib("1{2}", printableSymbols2)
        a.compile()
        a.search("1")
        self.assertEqual("", a.groups[0].processed)

    def test_repeating2(self):
        a = relibrary.MyRegLib("1{2}", printableSymbols2)
        a.compile()
        a.search("11")
        self.assertEqual("11", a.groups[0].processed)

    def test_repeating2(self):
        a = relibrary.MyRegLib("21{2}", printableSymbols2)
        a.compile()
        a.search("211")
        self.assertEqual("211", a.groups[0].processed)

    def test_repeating3(self):
        a = relibrary.MyRegLib("21{2}3", printableSymbols2)
        a.compile()
        a.search("2113")
        self.assertEqual("2113", a.groups[0].processed)

    def test_repeating4(self):
        a = relibrary.MyRegLib("21{2}3", printableSymbols2)
        a.compile()
        a.search("2113")
        self.assertEqual("2113", a.groups[0].processed)

    def test_repeating5(self):
        a = relibrary.MyRegLib("21{10}3", printableSymbols2)
        a.compile()
        a.search("2113")
        self.assertEqual("", a.groups[0].processed)

    def test_repeating6(self):
        a = relibrary.MyRegLib("21{10}3", printableSymbols2)
        a.compile()
        a.search("211111111113")
        self.assertEqual("211111111113", a.groups[0].processed)

    def test_repeating6(self):
        a = relibrary.MyRegLib("1|2{1}", printableSymbols2)
        a.compile()
        a.search("1")
        self.assertEqual("1", a.groups[0].processed)

    def test_repeating7(self):
        a = relibrary.MyRegLib("1|2{1}", printableSymbols2)
        a.compile()
        a.search("2")
        self.assertEqual("2", a.groups[0].processed)

    def test_repeating8(self):
        a = relibrary.MyRegLib("1|2{2}", printableSymbols2)
        a.compile()
        a.search("22")
        self.assertEqual("22", a.groups[0].processed)

    def test_repeating9(self):
        a = relibrary.MyRegLib("1|2{2}|123", printableSymbols2)
        a.compile()
        a.search("123")
        self.assertEqual("1", a.groups[0].processed)

    def test_repeating10(self):
        a = relibrary.MyRegLib("(:12){2}", printableSymbols2)
        a.compile()
        a.search("1212")
        self.assertEqual("1212", a.groups[0].processed)

    def test_repeating11(self):
        a = relibrary.MyRegLib("(:12|3){2}", printableSymbols2)
        a.compile()
        a.search("11264")
        self.assertEqual("", a.groups[0].processed)

    def test_repeating12(self):
        a = relibrary.MyRegLib("(:12|3){2}", printableSymbols2)
        a.compile()
        a.search("1212")
        self.assertEqual("1212", a.groups[0].processed)

    def test_repeating13(self):
        a = relibrary.MyRegLib("(:12|3){2}", printableSymbols2)
        a.compile()
        a.search("312")
        self.assertEqual("312", a.groups[0].processed)

    def test_repeating14(self):
        a = relibrary.MyRegLib("(:12|3){2}", printableSymbols2)
        a.compile()
        a.search("33")
        self.assertEqual("33", a.groups[0].processed)

    def test_repeating15(self):
        a = relibrary.MyRegLib("(:12|3){3}", printableSymbols2)
        a.compile()
        a.search("12123")
        self.assertEqual("12123", a.groups[0].processed)

    def test_repeating16(self):
        a = relibrary.MyRegLib("(:12|3){3}", printableSymbols2)
        a.compile()
        a.search("333")
        self.assertEqual("333", a.groups[0].processed)

    def test_repeating17(self):
        a = relibrary.MyRegLib("(:12|3){3}", printableSymbols2)
        a.compile()
        a.search("3312")
        self.assertEqual("3312", a.groups[0].processed)

    def test_repeating18(self):
        a = relibrary.MyRegLib("(:12|3){3}", printableSymbols2)
        a.compile()
        a.search("12312")
        self.assertEqual("12312", a.groups[0].processed)

    def test_repeating19(self):
        a = relibrary.MyRegLib("(:12|3){3}", printableSymbols2)
        a.compile()
        a.search("121213")
        self.assertEqual("", a.groups[0].processed)

    def test_repeating20(self):
        a = relibrary.MyRegLib("12|3{2}", printableSymbols2)
        a.compile()
        a.search("33")
        self.assertEqual("33", a.groups[0].processed)

    def test_choose1(self):
        a = relibrary.MyRegLib("[12]", printableSymbols2)
        a.compile()
        a.search("1")
        self.assertEqual("1", a.groups[0].processed)

    def test_choose2(self):
        a = relibrary.MyRegLib("[12]", printableSymbols2)
        a.compile()
        a.search("2")
        self.assertEqual("2", a.groups[0].processed)

    def test_choose3(self):
        a = relibrary.MyRegLib("[1234]", printableSymbols2)
        a.compile()
        a.search("4")
        self.assertEqual("4", a.groups[0].processed)

    def test_choose4(self):
        a = relibrary.MyRegLib("1[12]", printableSymbols2)
        a.compile()
        a.search("11")
        self.assertEqual("11", a.groups[0].processed)

    def test_choose5(self):
        a = relibrary.MyRegLib("1[12]3", printableSymbols2)
        a.compile()
        a.search("123")
        self.assertEqual("123", a.groups[0].processed)

    def test_choose6(self):
        a = relibrary.MyRegLib("1[12]|3", printableSymbols2)
        a.compile()
        a.search("12")
        self.assertEqual("12", a.groups[0].processed)

    def test_choose7(self):
        a = relibrary.MyRegLib("1[12]", printableSymbols2)
        a.compile()
        a.search("11")
        self.assertEqual("11", a.groups[0].processed)

    def test_choose8(self):
        a = relibrary.MyRegLib("1[21]", printableSymbols2)
        a.compile()
        a.search("11")
        self.assertEqual("11", a.groups[0].processed)

    def test_choose9(self):
        a = relibrary.MyRegLib("1[12]", printableSymbols2)
        a.compile()
        a.search("11")
        self.assertEqual("11", a.groups[0].processed)

    def test_choose10(self):
        a = relibrary.MyRegLib("[21]{2}", printableSymbols2)
        a.compile()
        a.search("12")
        self.assertEqual("12", a.groups[0].processed)

    def test_choose11(self):
        a = relibrary.MyRegLib("21{2}", printableSymbols2)
        a.compile()
        a.search("2121")
        self.assertEqual("", a.groups[0].processed)

    def test_choose11(self):
        a = relibrary.MyRegLib("21{2}", printableSymbols2)
        a.compile()
        a.search("2121")
        self.assertEqual("", a.groups[0].processed)

    def test_choose12(self):
        a = relibrary.MyRegLib("[qwertyui]{2}[qwertyui]", printableSymbols2)
        a.compile()
        a.search("qq12t")
        self.assertEqual("", a.groups[0].processed)

    def test_choose13(self):
        a = relibrary.MyRegLib("1…", printableSymbols2)
        a.compile()
        a.search("1")
        self.assertEqual("1", a.groups[0].processed)


if __name__ == '__main__':
    main()


