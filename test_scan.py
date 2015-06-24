import unittest

from line import Line
from letter import Letter, Vowel, ShortVowel, LongVowel
from cluster import ConsonantCluster
from syllable import Syllable
from scan import Scan, Dactyl, Spondee, TailSpondee, hexameter, make_scans, \
    eliminate_redundant_scans
from replace import ParseInto, Or
from word import WordInstance, WordForm
from source import Source
from misc import trace, dd, Multiple, Unknown
from testing import reduce_to_text

class TestScan(unittest.TestCase):

    maxDiff = None

    def test_dactyl(self):
        parser = ParseInto(
            Dactyl
        )

        line = Line('arma vi')
        parses = parser(line.syllables)
        self.assertEqual(len(parses), 1)
        parse = parses[0]

        self.assertEqual(
            reduce_to_text(parse),
            [
                Dactyl(
                    Syllable('a', ConsonantCluster('r')),
                    Syllable(ConsonantCluster('m'), 'a'),
                    Syllable(ConsonantCluster('v'), 'i')
                )
            ]
        )

        syllables = parse[0].syllables
        self.assertEqual(syllables[0].vowel.is_long, Unknown)
        self.assertEqual(syllables[1].vowel.is_long, False)
        self.assertEqual(syllables[2].vowel.is_long, False)

        self.assertCountEqual(
            reduce_to_text(parser(Line('arma vir').syllables)),
            Multiple()
        )

        scans = make_scans(line.syllables, parser)
        map = scans[0].syllable_map
        self.assertEqual(
            [map.is_stressed(sy) for sy in parse[0].syllables],
            [True, False, False]
        )

        self.assertEqual(
            scans[0].form_of(WordInstance('vi', Source(line, 1))),
            WordForm(
                Letter('v'),
                ShortVowel('i')
            )
        )

    def test_hexameter(self):
        line = Line('arma virumque cano troiae qui primus ab oris')
        self.assertCountEqual(
            [str(scan) for scan in line.scans],
            [
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ'-ĭ-/-æ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ-ĭ-/-ā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trō'-/-jæ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quē / cā'-nŏ trŏ'-/-jæ quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trŏ'-jă-/-ē quī / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quĕ că'-/-nō trō-/-jā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris",
"a'r-mă vĭ-/-ru'm-quē / cā'-nŏ trŏ-/-jā'-ĕ quĭ / prī'-mŭ-s⁀ă-/-b⁀ō'-ris"
            ]
        )

        self.assertCountEqual(
            line.scans[0].word_instances,
            [
                WordInstance('arma', Source(line, 0)),
                WordInstance('virumque', Source(line, 1)),
                WordInstance('cano', Source(line, 2)),
                WordInstance('troiae', Source(line, 3)),
                WordInstance('qui', Source(line, 4)),
                WordInstance('primus', Source(line, 5)),
                WordInstance('ab', Source(line, 6)),
                WordInstance('oris', Source(line, 7))
            ]
        )

        expect = frozenset([
            WordForm(
                Vowel('a'),
                Letter('r'),
                Letter('m'),
                ShortVowel('a')
            ),
            WordForm(
                Letter('v'),
                ShortVowel('i'),
                Letter('r'),
                Vowel('u'),
                Letter('m'),
                Letter('qu'),
                ShortVowel('e')
            ),
            WordForm(
                Letter('c'),
                ShortVowel('a'),
                Letter('n'),
                LongVowel('o')
            ),
            WordForm(
                Letter('t'),
                Letter('r'),
                ShortVowel('o'),
                Letter('j'),
                ShortVowel('a'),
                LongVowel('e')
            ),
            WordForm(
                Letter('qu'),
                LongVowel('i')
            ),
            WordForm(
                Letter('p'),
                Letter('r'),
                LongVowel('i'),
                Letter('m'),
                ShortVowel('u'),
                Letter('s')
            ),
            WordForm(
                ShortVowel('a'),
                Letter('b')
            ),
            WordForm(
                LongVowel('o'),
                Letter('r'),
                Vowel('i'),
                Letter('s')
            )
        ])
        self.assertTrue(expect in [scan.word_forms for scan in line.scans])

    def test_eliminate_redundant_scans(self):
        parser = ParseInto(
            Spondee
        )
        line = Line('uscra')
        scans = make_scans(line.syllables, parser)

        # If this assertion fails, the following assertion is meaningless.
        self.assertCountEqual(  
            [str(scan) for scan in scans],
            [
                "ū'-scrā",
                "u's-crā",
                "u'sc-rā",
            ]
        )

        self.assertCountEqual(
            [str(e) for e in eliminate_redundant_scans(scans)],
            [
                "ū'-scrā",
                "u's-crā",
            ]
        )


class TestScanset(unittest.TestCase):

    maxDiff = None

    def test_basics(self):
        parser = ParseInto(
            Spondee
        )
        line = Line('uscra')
        scanset = eliminate_redundant_scans(make_scans(line.syllables, parser))
        self.assertCountEqual(
            scanset.word_forms,
            [
                WordForm(
                    Vowel('u'),
                    Letter('s'),
                    Letter('c'),
                    Letter('r'),
                    LongVowel('a')
                ),
                WordForm(
                    LongVowel('u'),
                    Letter('s'),
                    Letter('c'),
                    Letter('r'),
                    LongVowel('a')
                )
            ]
        )

        self.assertCountEqual(
            set(
                [word_form.dictionary_word for word_form in scanset.word_forms]
            ),
            [
                'uscra'
            ]
        )

        self.assertEqual(
            scanset.proportion_containing(
                WordInstance('uscra', Source(line, 0)),
                WordForm(
                    LongVowel('u'),
                    Letter('s'),
                    Letter('c'),
                    Letter('r'),
                    LongVowel('a')
                )
            ),
            0.5
        )

    def teest_bad_scan(self):
        pass # FIXME
        # nudavit caecumque domus scelus omne retexit


if __name__ == '__main__':
    unittest.main()

