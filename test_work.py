import unittest
from io import StringIO

from work import Work
from misc import trace, dd, Multiple


mock_file = StringIO("""

First line

Second line


""")

class TestWork(unittest.TestCase):

    maxDiff = None

    def teest_basics(self):
        work = Work(mock_file, 'Mockeid 1')
        i = iter(work)
        line1 = next(i)
        self.assertEqual(line1.original_text, 'First line')
        self.assertEqual(line1.work, work)
        self.assertEqual(line1.line_num, 1)
        line2 = next(i)
        self.assertEqual(line2.original_text, 'Second line')
        self.assertEqual(line2.work, work)
        self.assertEqual(line2.line_num, 2)
