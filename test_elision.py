import unittest

from line import Line, Multiple
from word import WordInstance
from letter import Letter
from elision import Elision, hiatus, generate_elisions
from testing import strip_sources, reduce_to_text
from misc import trace, dd


class TestElision(unittest.TestCase):

    maxDiff = None

    def test_no_elision(self):
        self.assertCountEqual(
            reduce_to_text(Line('non ego').with_elisions),
            Multiple(
                ['n', 'o', 'n', 'e', 'g', 'o']
            )
        )

    def test_simplest(self):
        line = Line('re id')

        letters = generate_elisions(line.letters)
        self.assertEqual(letters[0][0].__class__, Letter)
        self.assertCountEqual(
            reduce_to_text(letters),
            Multiple(
                ['r', Elision('e'), 'i', 'd'],
                ['r', 'e', hiatus, 'i', 'd'],
            )
        )

        self.assertCountEqual(
            [' '.join(str(letter) for letter in e)
                for e in line.with_elisions
            ],
            [
                'r(e) i d',
                'r e i d'
            ]
        )

    def test_two_elisions(self):
        line = Line('rem hida it')

        letters = generate_elisions(line.letters)
        self.assertCountEqual(
            reduce_to_text(letters),
            Multiple(
                ['r', Elision('e', 'm', 'h'), 'i', 'd', Elision('a'), 'i', 't'],
                ['r', 'e', 'm', hiatus, 'h', 'i', 'd', Elision('a'), 'i', 't'],
                ['r', Elision('e', 'm', 'h'), 'i', 'd', 'a', hiatus, 'i', 't'],
                ['r', 'e', 'm', hiatus, 'h', 'i', 'd', 'a', hiatus, 'i', 't'],
            )
        )

    def test_am_or(self):
        self.assertCountEqual(
            reduce_to_text(Line('am or').with_elisions),
            Multiple(
                ['a', 'm', 'o', 'r']
            )
        )



if __name__ == '__main__':
    unittest.main()
