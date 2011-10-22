#! /usr/bin/env /usr/local/bin/python

#import test_support
#from test_support import TestFailed, have_unicode
import unittest
import sys

from pyx12.validation import IsValidDataType
from pyx12.errors import *

class BasicNumeric(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'N', 'B'))
        self.failUnless(IsValidDataType('-1', 'N', 'B'))
        self.failUnless(IsValidDataType('10', 'N', 'B'))
        self.failUnless(IsValidDataType('-10', 'N', 'B'))
        self.failUnless(IsValidDataType('0000500', 'N', 'B'))
        self.failUnless(IsValidDataType('1', 'R', 'B'))

    def testInvalid(self):
        self.failIf(IsValidDataType('+10', 'N', 'B'))
        self.failIf(IsValidDataType('1.', 'N', 'B'))
        self.failIf(IsValidDataType('-1.', 'N', 'B'))


class BasicReal(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('-331232', 'R', 'B'))
        self.failUnless(IsValidDataType('1.325', 'R', 'B'))
        self.failUnless(IsValidDataType('.024', 'R', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('+331232', 'R', 'B'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'B'))
        self.failIf(IsValidDataType('333.', 'R', 'B'))
        self.failIf(IsValidDataType('a.603', 'R', 'B'))
        self.failIf(IsValidDataType('0.0b', 'R', 'B'))


class BasicIdentifier(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('10&3', 'ID', 'B'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('abc', 'ID', 'B'))
        self.failIf(IsValidDataType('abc   ', 'ID', 'B'))

class BasicString(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('LKJS', 'AN', 'B'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'B'))
        self.failUnless(IsValidDataType(r"""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'B'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('abd1P', 'AN', 'B'))
        self.failIf(IsValidDataType(r'extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'B'))
        self.failIf(IsValidDataType(r"""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'B'))
        self.failIf(IsValidDataType('bad ^`', 'AN', 'B'))
        self.failIf(IsValidDataType('wharf', 'AN', 'B'))
        self.failIf(IsValidDataType('\\', 'AN', 'B'))


class BasicDate(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'B'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'B'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'B'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'B'))
        self.failUnless(IsValidDataType('020414', 'DT', 'B'))
        self.failUnless(IsValidDataType('960229', 'DT', 'B'))
        self.failUnless(IsValidDataType('200402020400', 'DT', 'B'))
        self.failUnless(IsValidDataType('20040430', 'DT', 'B'))
        self.failUnless(IsValidDataType('20040401-20040430', 'RD8', 'B'))
        
    def testInvalidLeapDate(self):
        self.failIf(IsValidDataType('990229', 'DT', 'B'))
        self.failIf(IsValidDataType('20030229', 'DT', 'B'))
        self.failIf(IsValidDataType('19000229', 'DT', 'B'))

    def testInvalidAlpha(self):
        self.failIf(IsValidDataType('200204a', 'DT', 'B'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'B'))

    def testInvalidMonth(self):
        self.failIf(IsValidDataType('19991301', 'DT', 'B'))
        self.failIf(IsValidDataType('030732', 'DT', 'B'))

    def testInvalidDay(self):
        self.failIf(IsValidDataType('19992377', 'DT', 'B'))
        self.failIf(IsValidDataType('19991277', 'DT', 'B'))
        self.failIf(IsValidDataType('20040431', 'DT', 'B'))

    def testInvalidLength(self):
        self.failIf(IsValidDataType('200402024 00', 'DT', 'B'))
        self.failIf(IsValidDataType('200422024000', 'DT', 'B'))
        self.failIf(IsValidDataType('20040222040', 'DT', 'B'))
        self.failIf(IsValidDataType('2004022204', 'DT', 'B'))
        self.failIf(IsValidDataType('200402220', 'DT', 'B'))

    def testInvalidChar(self):
        self.failIf(IsValidDataType('-20040430', 'RD8', 'B'))
        self.failIf(IsValidDataType('20040430-', 'RD8', 'B'))

    def testInvalidAncient(self):
        self.failIf(IsValidDataType('17992301', 'DT', 'B'))
        self.failIf(IsValidDataType('09991202', 'DT', 'B'))


class BasicTime(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'B'))
        self.failUnless(IsValidDataType('000159', 'TM', 'B'))

    def testInvalid(self):
        self.failIf(IsValidDataType('07315a', 'TM', 'B'))
        self.failIf(IsValidDataType('7 31', 'TM', 'B'))
        self.failIf(IsValidDataType('7:31', 'TM', 'B'))


class ExtendedNumeric(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'N', 'E'))
        self.failUnless(IsValidDataType('-1', 'N', 'E'))
        self.failUnless(IsValidDataType('10', 'N', 'E'))
        self.failUnless(IsValidDataType('-10', 'N', 'E'))
        self.failUnless(IsValidDataType('0000500', 'N', 'E'))

    def testInvalid(self):
        self.failIf(IsValidDataType('+10', 'N', 'E'))
        self.failIf(IsValidDataType('1.', 'N', 'E'))
        self.failIf(IsValidDataType('-1.', 'N', 'E'))


class ExtendedReal(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('1', 'R', 'E'))
        self.failUnless(IsValidDataType('-331232', 'R', 'E'))
        self.failUnless(IsValidDataType('1.325', 'R', 'E'))
        self.failUnless(IsValidDataType('.024', 'R', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('a.603', 'R', 'E'))
        self.failIf(IsValidDataType('0.0b', 'R', 'E'))
        self.failIf(IsValidDataType('+331232', 'R', 'E'))
        self.failIf(IsValidDataType('123,456,789.123', 'R', 'E'))
        self.failIf(IsValidDataType('333.', 'R', 'E'))


class ExtendedIdentifier(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('abc', 'ID', 'E'))
        self.failUnless(IsValidDataType('10&3', 'ID', 'E'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'E'))
        self.failUnless(IsValidDataType('abc   ', 'ID', 'E'))


class ExtendedString(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'E'))
        self.failUnless(IsValidDataType('abd1P', 'AN', 'E'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'E'))
        self.failUnless(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E'))
        self.failUnless(IsValidDataType('extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E'))
        self.failUnless(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E'))
        self.failUnless(IsValidDataType('wharf', 'AN', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('bad ^`', 'AN', 'E'))


class ExtendedDate(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('20010418', 'DT', 'E'))
        self.failUnless(IsValidDataType('20030429', 'DT', 'E'))
        self.failUnless(IsValidDataType('19040229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20000229', 'DT', 'E'))
        self.failUnless(IsValidDataType('20040229', 'DT', 'E'))
        self.failUnless(IsValidDataType('020414', 'DT', 'E'))
        self.failUnless(IsValidDataType('960229', 'DT', 'E'))
        self.failUnless(IsValidDataType('200402020400', 'DT', 'B'))
        self.failUnless(IsValidDataType('20010418', 'D8', 'E'))
        self.failUnless(IsValidDataType('20030429', 'D8', 'E'))
        self.failUnless(IsValidDataType('19040229', 'D8', 'E'))
        self.failUnless(IsValidDataType('20000229', 'D8', 'E'))
        self.failUnless(IsValidDataType('20040229', 'D8', 'E'))
        self.failUnless(IsValidDataType('020414', 'D6', 'E'))
        self.failUnless(IsValidDataType('960229', 'D6', 'E'))
        self.failUnless(IsValidDataType('20040401-20040430', 'RD8', 'E'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('990229', 'DT', 'E'))
        self.failIf(IsValidDataType('030732', 'DT', 'E'))
        self.failIf(IsValidDataType('19992377', 'DT', 'E'))
        self.failIf(IsValidDataType('19991277', 'DT', 'E'))
        self.failIf(IsValidDataType('200204a', 'DT', 'E'))
        self.failIf(IsValidDataType('2002041a', 'DT', 'E'))
        self.failIf(IsValidDataType('19000229', 'DT', 'E'))
        self.failIf(IsValidDataType('20030229', 'DT', 'E'))
        self.failIf(IsValidDataType('200402024 00', 'DT', 'B'))

        self.failIf(IsValidDataType('990229', 'D6', 'E'))
        self.failIf(IsValidDataType('030732', 'D6', 'E'))
        self.failIf(IsValidDataType('19992377', 'D8', 'E'))
        self.failIf(IsValidDataType('19991277', 'D8', 'E'))
        self.failIf(IsValidDataType('200204a', 'D8', 'E'))
        self.failIf(IsValidDataType('2002041a', 'D8', 'E'))
        self.failIf(IsValidDataType('19000229', 'D8', 'E'))
        self.failIf(IsValidDataType('20030229', 'D8', 'E'))
        self.failIf(IsValidDataType('55555555', 'D8', 'E'))
        self.failIf(IsValidDataType('55555555', 'D8', 'B'))
        self.failIf(IsValidDataType('200402024 00', 'D8', 'B'))
        self.failIf(IsValidDataType('020414', 'D8', 'E'))
        self.failIf(IsValidDataType('20020414', 'D6', 'E'))
        self.failIf(IsValidDataType('-20040430', 'RD8', 'E'))
        self.failIf(IsValidDataType('20040430-', 'RD8', 'E'))

    def testInvalidAncient(self):
        self.failIf(IsValidDataType('17992301', 'DT', 'E'))
        self.failIf(IsValidDataType('09991202', 'DT', 'E'))
        self.failIf(IsValidDataType('17992301', 'D8', 'E'))
        self.failIf(IsValidDataType('09991202', 'D8', 'E'))


class ExtendedTime(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('0731', 'TM', 'E'))
        self.failUnless(IsValidDataType('000159', 'TM', 'E'))

    def testInvalid(self):
        self.failIf(IsValidDataType('07315a', 'TM', 'E'))
        self.failIf(IsValidDataType('7 31', 'TM', 'B'))
        self.failIf(IsValidDataType('7:31', 'TM', 'B'))


class Extendedi5010Identifier(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('abc', 'ID', 'E', '00501'))
        self.failUnless(IsValidDataType('10&3', 'ID', 'E', '00501'))
        self.failUnless(IsValidDataType('  XYZ', 'ID', 'E', '00501'))
        self.failUnless(IsValidDataType('abc   ', 'ID', 'E', '00501'))


class Extended5010String(unittest.TestCase):
    def testValid(self):
        self.failUnless(IsValidDataType('LKJS\\', 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType('abd1P', 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType('THIS IS A TEST ()', 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType("""BASIC ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?=""", 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType('extended abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$', 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType("""Both ABCDEFIGHIJKLMNOPQRSTUVWXYZ 0123456789!"&'()+,-./;:?= abcdefghijklmnopqrstuvwxyz%~@[]_{}\|<>#$""", 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType('wharf', 'AN', 'E', '00501'))
        self.failUnless(IsValidDataType('_good ^`', 'AN', 'E', '00501'))
        
    def testInvalid(self):
        self.failIf(IsValidDataType('%s'%(chr(0x1D)), 'AN', 'E', '00501'))
