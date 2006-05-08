# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Author: Eray Ozkural <eray at pardus.org.tr>

import unittest
import os
import random
import array

from pisi.zipfileext import *

import testcase

def listtostr(list):
    return array.array('B', list).tostring()

class ZipFileExtCase(testcase.TestCase):

    def setUp(self):
        testcase.TestCase.setUp(self, database = False)

    def makeRandomFile(self, fn):
        random.seed()
        str = listtostr( [ random.randint(0, 255) for x in range(2048) ] )
        f = file(fn, 'w')
        f.write(str)
        return str
    
    def testDeflateZipUnzip(self):
        str = self.makeRandomFile('tmp/random')
        zipfile = ZipFile('tmp/test.zip', 'w')
        zipfile.write('tmp/random', compress_type = ZIP_DEFLATED)
        zipfile.close()
        zipfile2 = ZipFile('tmp/test.zip', 'r')
        str2 = zipfile2.read('tmp/random')
        self.assertEqual(str, str2)

suite = unittest.makeSuite(ZipFileExtCase)
