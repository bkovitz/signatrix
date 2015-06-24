import unittest

from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    ignore_matched_input, TestVar, Optional, NotFollowedBy, \
    CombinatoricSequence, CombinatoricAlternatives
from source import Source
from word import WordInstance
from letter import Letter, is_consonant
from misc import Multiple
from testing import reduce_to_text


class MockSource(Source):

    def __init__(self, index=None):
        super().__init__(self, index)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.index == other.index
        )

    def __repr__(self):
        return 'MockSource(%s)' % repr(self.index)


mockSource = MockSource()


class TestTarget(unittest.TestCase):

    def test_qu(self):
        target = Target('q', 'u')
        env = {}

        x = ('q', 'u', 'a', 'e')
        self.assertEqual(
            (['q', 'u'], ('a', 'e'), {}),
            target.match(x, env)
        )

        x = ('x', 'y')
        self.assertEqual(
            (None, None, None),
            target.match(x, env)
        )

        x = ()
        self.assertEqual(
            (None, None, None),
            target.match(x, env)
        )

    def test_A(self):
        target = Target(Var('A', Any))
        env = {}
        x = ('q', 'u', 'a', 'e')
        self.assertEqual(
            (['q'], ('u', 'a', 'e'), {'A': ['q']}),
            target.match(x, env)
        )

    def test_letter(self):
        target = Target('a')
        env = {}
        x = (Letter('a', mockSource), Letter('b', mockSource))
        self.assertEqual(
            ([Letter('a', mockSource)], (Letter('b', mockSource),), {}),
            target.match(x, env)
        )


class TestReplaceWith(unittest.TestCase):

    def test_literal(self):
        rw = ReplaceWith(['qu'])
        self.assertCountEqual(
            (
                ['qu'],
            ),
            rw.replace(ignore_matched_input, (), {})
        )

    def test_variable(self):
        rw = ReplaceWith([Var('A')])
        self.assertCountEqual(
            (
                ['x'],
            ),
            rw.replace(ignore_matched_input, (), {'A': 'x'})
        )


class TestCombinatoricMap(unittest.TestCase):

    maxDiff = None

    def test_basics(self):
        qu_map = CombinatoricMap(lambda rw_object, source: rw_object,
            (Target('q', 'u'), ReplaceWith(['qu'])),
            (Target('q', 'v'), ReplaceWith(['qu'])),
            (Target('a', 'e'), ReplaceWith(['ae'], ['a', 'e'])),
            (Target(Var('A', Any)), ReplaceWith([Var('A')]))
        )

        qvaec = ('q', 'v', 'a', 'e', 'c')

        self.assertCountEqual(
            qu_map.map(qvaec),
            (
                ('qu', 'a', 'e', 'c'),
                ('qu', 'ae', 'c')
            )
        )

    def test_with_source(self):
        qu_map = CombinatoricMap(MakeInto(Letter),
            (Target('q', 'u'), ReplaceWith(('qu',))),
            (Target('q', 'v'), ReplaceWith(('qu',))),
            (Target('a', 'e'), ReplaceWith(('ae',), ('a', 'e'))),
            (Target(Var('A', Any)), ReplaceWith((Var('A'),)))
        )

        word_instance = WordInstance('qvaec', mockSource)
        qvaec = (
            Letter('q', Source(word_instance, 0)),
            Letter('v', Source(word_instance, 1)),
            Letter('a', Source(word_instance, 2)),
            Letter('e', Source(word_instance, 3)),
            Letter('c', Source(word_instance, 4))
        )
        self.assertCountEqual(
            qu_map.map(qvaec),
            (
                (
                    Letter('qu', Source(word_instance, 0)),
                    Letter('a', Source(word_instance, 2)),
                    Letter('e', Source(word_instance, 3)),
                    Letter('c', Source(word_instance, 4)),
                ),
                (
                    Letter('qu', Source(word_instance, 0)),
                    Letter('ae', Source(word_instance, 2)),
                    Letter('c', Source(word_instance, 4)),
                )
            )
        )

    def test_testvar(self):
        c_map = CombinatoricMap(MakeInto(Letter),
            (Target('a', TestVar('C', is_consonant), 'e'),
                ReplaceWith(['A', Var('C'), 'E'])),
            (Target(Var('A', Any)),
                ReplaceWith([Var('A')]))
        )

        input = 'garebaie'

        self.assertCountEqual(
            reduce_to_text(c_map.map(input)),
            (
                ['g', 'A', 'r', 'E', 'b', 'a', 'i', 'e'],
            )
        )

    def test_optional(self):
        c_map = CombinatoricMap(ignore_matched_input, 
            (Target(Optional('a'), 'b'),
                ReplaceWith(['AB'])),
            (Target(Var('A', Any)),
                ReplaceWith([Var('A')]))
        )

        input = 'xybxabac'

        self.assertCountEqual(
            c_map.map(input),
            (
                ('x', 'y', 'AB', 'x', 'AB', 'a', 'c'),
            )
        )

    def test_not_followed_by(self):
        c_map = CombinatoricMap(ignore_matched_input,
            (Target('a', NotFollowedBy('b')),
                ReplaceWith(('A',))),
            (Target(Var('A', Any)),
                ReplaceWith((Var('A'),)))
        )

        input = 'axabc'

        self.assertCountEqual(
            c_map.map(input),
            (
                ('A', 'x', 'a', 'b', 'c'),
            )
        )


class TestCombinatorics(unittest.TestCase):

    maxDiff = None

    def test_basics(self):
        seq = CombinatoricSequence()
        seq = seq.append(CombinatoricAlternatives(['a', 'b', 'c'], ['A']))
        seq = seq.append(CombinatoricAlternatives('d'))
        self.assertEqual(
            seq.product,
            Multiple(
                (['a', 'b', 'c'], 'd'),
                (['A'], 'd')
            )
        )

if __name__ == '__main__':
    unittest.main()

