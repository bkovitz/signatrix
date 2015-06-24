import unittest

from line import Line, Multiple
from word import WordInstance
from letter import Letter
from testing import strip_sources, reduce_to_text
from misc import trace, dd, Unknown, Incompatible


class TestLetter(unittest.TestCase):

    maxDiff = None

    def test_aut(self):
        line = Line('aut')
        letters = line.letters
        self.assertCountEqual(
            strip_sources(letters),
            Multiple(
                [
                    Letter('au'),
                    Letter('t'),
                ],
                [
                    Letter('a'),
                    Letter('u'),
                    Letter('t')
                ]
            )
        )

        au, t = letters[0]  # arbitrary index; OK if 1
        self.assertEqual(au.is_long, True)
        with self.assertRaises(Incompatible) as cm:
            short_au = au.make_short()

        a, u, t = letters[1]  # as above
        self.assertEqual(a.is_long, Unknown)
        short_a = a.make_short()
        self.assertEqual(short_a.is_long, False)
        self.assertEqual(short_a.is_short, True)
        long_a = a.make_long()
        self.assertEqual(long_a.is_long, True)
        self.assertEqual(long_a.is_short, False)

    def test_julius(self):
        self.assertCountEqual(
            reduce_to_text(Line('Julius').letters),
            Multiple(
                ['i', 'u', 'l', 'i', 'u', 's'],
                ['i', 'u', 'l', 'j', 'u', 's'],
                ['j', 'u', 'l', 'i', 'u', 's'],
                ['j', 'u', 'l', 'j', 'u', 's'],
            )
        )

    def test_bis(self):
        self.assertCountEqual(
            reduce_to_text(Line('bis').letters),
            [
                ['b', 'i', 's'],
            ]
        )

    def test_ait(self):
        self.assertCountEqual(
            reduce_to_text(Line('ait').letters),
            [
                ['a', 'i', 't'],
            ]
        )

    def test_cui(self):
        self.assertCountEqual(
            reduce_to_text(Line('cui').letters),
            (
                ['c', 'uj'],
                ['c', 'u', 'i']
            )
        )

    def test_mori(self):
        self.assertCountEqual(
            reduce_to_text(Line('vmori').letters),
            [
                ['u', 'm', 'o', 'r', 'i'],
                # vmorj, etc. are not possible
            ]
        )

    def test_laviniaque(self):
        self.assertCountEqual(
            reduce_to_text(Line('laviniaque').letters),
            [
                ['l', 'a', 'v', 'i', 'n', 'i', 'a', 'qu', 'e'],
                ['l', 'a', 'v', 'i', 'n', 'j', 'a', 'qu', 'e'],
                ['l', 'au', 'i', 'n', 'i', 'a', 'qu', 'e'],
                ['l', 'au', 'i', 'n', 'j', 'a', 'qu', 'e'],
                ['l', 'a', 'u', 'i', 'n', 'i', 'a', 'qu', 'e'],
                ['l', 'a', 'u', 'i', 'n', 'j', 'a', 'qu', 'e'],
            ]
        )
