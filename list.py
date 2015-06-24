import itertools

from misc import lazy, trace, dd


class TriedToCarEmptyList(RuntimeError): pass
class TriedToCdrEmptyList(RuntimeError): pass

class List:
    def __init__(self, *elems):
        if len(elems) == 0:
            self.__class__ = Nil
        elif len(elems) == 1:
            self.car = elems[0]
            self._cdr = lambda: nil
        else:
            self.car = elems[0]
            self._cdr = lazy(lambda: List(*elems[1:]))

    @property
    @lazy
    def cdr(self):
        return self._cdr()

    is_nil = False

    @property
    @lazy
    def to_ordinary_tuple(self):
        if self.cdr.is_nil:
            return (self.car,)
        else:
            return (self.car,) + self.cdr.to_ordinary_tuple
        
    def __iter__(self):
        return iter(self.to_ordinary_tuple)

    def __eq__(self, other):
        return self.to_ordinary_tuple == other.to_ordinary_tuple

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return 'List(%s)' % (
            ', '.join(repr(elem) for elem in self.to_ordinary_tuple)
        )


class Nil(List):
    @property
    def car(self):
        raise(TriedToCarEmptyList)

    @property
    def cdr(self):
        raise(TriedToCdrEmptyList)

    to_ordinary_tuple = ()

    is_nil = True

    def __hash__(self):
        return hash(())

    def __eq__(self, other):
        return other.is_nil

    def __repr__(self):
        return 'nil'

nil = Nil()


import unittest

class TestList(unittest.TestCase):

    def test_basics(self):
        l = List('A', 'B', 'C')
        m = List('A', 'B')

        self.assertEqual(l.to_ordinary_tuple, ('A', 'B', 'C'))

        self.assertEqual(l, l)
        self.assertNotEqual(l, m)
        self.assertEqual(l.car, 'A')
        self.assertEqual(l.cdr, List('B', 'C'))

        self.assertNotEqual(l.cdr.cdr, nil)
        self.assertNotEqual(nil, l.cdr.cdr)
        self.assertEqual(m.cdr.cdr, nil)
        self.assertEqual(nil, m.cdr.cdr)


if __name__ == '__main__':
    unittest.main()

