import unittest

from line import Line, Multiple
from word import WordInstance
from letter import Letter
from source import Source

class TestLine(unittest.TestCase):

    maxDiff = None

    arma = Line('   arma  VIRUmQue ca5no <; ')
    qvae = Line('qvae')

    def test_text(self):
        self.assertEqual('arma virumque cano', self.arma.text)

    def test_words(self):
        self.assertEqual(
            (
                WordInstance('arma', Source(self.arma, 0)),
                WordInstance('virumque', Source(self.arma, 1)),
                WordInstance('cano', Source(self.arma, 2))
            ),
            self.arma.word_instances
        )

    def test_letters(self):
        word_instance = self.qvae.word_instances[0]

        self.assertCountEqual(
            Multiple(
                (
                    Letter('qu', Source(word_instance, 0)),
                    Letter('a', Source(word_instance, 2)),
                    Letter('e', Source(word_instance, 3))
                ),
                (
                    Letter('qu', Source(word_instance, 0)),
                    Letter('ae', Source(word_instance, 2))
                )
            ),
            self.qvae.letters
        )

if __name__ == '__main__':
    unittest.main()
