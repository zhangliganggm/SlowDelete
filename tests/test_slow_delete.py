# -*- encoding:UTF-8 -*-
__author__ = 'ACE'

import unittest
import slowdelete


class SlowDeleteFileTestCase(unittest.TestCase):
    """Test"""

    def setUp(self):
        self.filename = ur'big.file'
        frw = open(self.filename, "wb")

        # Create File Size = 0.25 GB
        for a in xrange(1024/4):
            frw.write('\0'*1024*1024)
        frw.close()

    def test_delete_5_mbs(self):
        """slow delete file speed = 5mb/s"""
        a = slowdelete.SlowDelete(self.filename)
        assert a.start() == True


if __name__ == '__main__':
    unittest.main()
