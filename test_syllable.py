import unittest

from line import Line
from cluster import ConsonantCluster
from syllable import Syllable
from misc import trace, dd, Multiple, Unknown
from testing import strip_sources, reduce_to_text

class TestSyllable(unittest.TestCase):

    maxDiff = None

    def test_amo(self):
        self.assertCountEqual(
            reduce_to_text(Line('amo').syllables),
            Multiple(
                [
                    Syllable('a'),
                    Syllable(ConsonantCluster('m'), 'o')
                ]
            )
        )

    def test_amor(self):
        line = Line('amor')
        syllables = line.syllables
        self.assertCountEqual(
            reduce_to_text(syllables),
            Multiple(
                [
                    Syllable('a'),
                    Syllable(ConsonantCluster('m'), 'o', ConsonantCluster('r'))
                ]
            )
        )

        a, mor = syllables[0]

        self.assertEqual(reduce_to_text(a.vowel), 'a')
        self.assertTrue(a.is_open)
        self.assertFalse(a.is_closed)
        self.assertTrue(a.could_be_heavy)
        self.assertTrue(a.could_be_light)
        self.assertEqual(a.vowel.is_long, Unknown)

        self.assertEqual(reduce_to_text(mor.vowel), 'o')
        self.assertFalse(mor.is_open)
        self.assertTrue(mor.is_closed)
        self.assertTrue(mor.could_be_heavy)
        self.assertFalse(mor.could_be_light)

        #print(mor)

#        heavy_a = a.make_heavy()
#        self.assertEqual(heavy_a.vowel, 

        #print(repr(no.vowel.word_instance))
        #print(repr(no.vowel.word_instance.line))

    def test_non_ego(self):
        line = Line('non ego')
        syllables = line.syllables
        self.assertCountEqual(
            reduce_to_text(syllables),
            Multiple(
                [
                    Syllable(ConsonantCluster('n'), 'o'),
                    Syllable(ConsonantCluster('n'), 'e'),
                    Syllable(ConsonantCluster('g'), 'o')
                ]
            )
        )

    def test_tenebra(self):
        self.assertCountEqual(
            reduce_to_text(Line('tenebra').syllables),
            Multiple(
                [
                    Syllable(ConsonantCluster('t'), 'e'),
                    Syllable(ConsonantCluster('n'), 'e'),
                    Syllable(ConsonantCluster('b', 'r'), 'a')
                ],
                [
                    Syllable(ConsonantCluster('t'), 'e'),
                    Syllable(ConsonantCluster('n'), 'e', ConsonantCluster('b')),
                    Syllable(ConsonantCluster('r'), 'a')
                ]
            )
        )
                
    def test_urbsa(self):
        self.assertCountEqual(
            reduce_to_text(Line('urbsa').syllables),
            Multiple(
                [
                    Syllable('u', ConsonantCluster('r', 'b')),
                    Syllable(ConsonantCluster('s'), 'a')
                ]
            )
        )

    def test_multum_ille(self):
        line = Line('multum ille')
        self.assertCountEqual(
            [' '.join(str(sy) for sy in syllables)
                for syllables in line.syllables
            ],
            [
                "mul t(um)⁀il le",
                "mul tu m⁀il le",
            ]
        )

    def test_gus_la(self):
        line = Line('gus la')
        self.assertCountEqual(
            [' '.join(str(sy) for sy in syllables)
                for syllables in line.syllables
            ],
            [
                "gu s⁀la",
                "gus la",
            ]
        )


if __name__ == '__main__':
    unittest.main()

