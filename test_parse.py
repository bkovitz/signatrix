import unittest

from replace import ParseInto, Chunk, Target, Var, Make, Any, Or
from source import Source
from word import WordInstance
from letter import Letter, is_consonant
from misc import Multiple
from testing import reduce_to_text


class TestParseInto(unittest.TestCase):

    def test_basics(self):
        class AB:
            def __init__(self, *contents):
                self.contents = contents
            def __eq__(self, other):
                return self.contents == other.contents
            def __repr__(self):
                return 'AB(%s)' % ', '.join(repr(c) for c in self.contents)

        parser = ParseInto(
            Chunk(
                old=['a'],
                new=[['a']]
            ),
            Chunk(
                old=['a', 'b'],
                new=[[Make(AB, *[Var('OLD')])]]
            ),
            Chunk(
                old=['c'],
                new=[['c']]
            )
        )

        self.assertCountEqual(
            parser(['a', 'a', 'b', 'c']),
            Multiple(
                ('a', AB('a', 'b'), 'c')
            )
        )

    def test_or(self):
        parser = ParseInto(
            Or(['a', 'b', 'c'], ['a', 'b']),
            Chunk(old=['d'], new=[['d']])
        )

        self.assertCountEqual(
            parser(['a', 'b', 'c', 'd']),
            Multiple(
                (['a', 'b', 'c'], 'd')
            )
        )

    def test_or2(self):
        parser = ParseInto(
            Or(['a', 'b', 'c'], ['a', 'b']),
            Or(['c', 'd'], ['d'])
        )

        self.assertCountEqual(
            parser(['a', 'b', 'c', 'd']),
            Multiple(
                (['a', 'b', 'c'], ['d']),
                (['a', 'b'], ['c', 'd'])
            )
        )


if __name__ == '__main__':
    unittest.main()

