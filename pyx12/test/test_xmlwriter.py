import os.path
import sys
import os
import unittest

try:
    from StringIO import StringIO
except:
    from io import StringIO

import tempfile

from pyx12.xmlwriter import XMLWriter


class TestWriter(unittest.TestCase):
    """
    """
    def setUp(self):
        self.res = '<?xml version="1.0" encoding="utf-8"?><x12err></x12err>'

    def test_write1(self):
        try:
            fd = StringIO(encoding='ascii')
            #print('CASE 1:')
        except:
            fd = StringIO()
            #print('CASE 2:')
        writer = XMLWriter(fd)
        writer.push("x12err")

        while len(writer) > 0:
            writer.pop()
        self.assertEqual(fd.getvalue(), self.res)
        fd.close()

    def test_write_temp(self):
        (fdesc, filename) = tempfile.mkstemp('.xml', 'pyx12_')
        with open(filename, 'w') as fd:
            writer = XMLWriter(fd)
            writer.push("x12err")

            while len(writer) > 0:
                writer.pop()

        with open(filename, 'r') as fd:
            self.assertEqual(fd.read(), self.res)

        try:
            os.remove(filename)
        except:
            pass
