import unittest

from word import WordForm
from letter import Letter, Vowel, LongVowel, ShortVowel

class TestWordForm(unittest.TestCase):

    def test_vowel_neq_longvowel(self):
        self.assertNotEqual(
            WordForm(
                LongVowel('u'),
                Letter('s'),
                Letter('c'),
                Letter('r'),
                LongVowel('a')
            ),
            WordForm(
                Vowel('u'),
                Letter('s'),
                Letter('c'),
                Letter('r'),
                LongVowel('a')
            )
        )

    def test_shortvowel_neq_longvowel(self):
        self.assertNotEqual(
            WordForm(
                LongVowel('u'),
                Letter('s'),
                Letter('c'),
                Letter('r'),
                LongVowel('a')
            ),
            WordForm(
                ShortVowel('u'),
                Letter('s'),
                Letter('c'),
                Letter('r'),
                LongVowel('a')
            )
        )
