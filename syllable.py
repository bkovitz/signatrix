from itertools import chain, product
import logging

from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    CanMatchTargetElem, Disallow, Filter, TestVar, ignore_matched_input, \
    Make, Optional, NotFollowedBy
from source import Source, HasSource, force_source_from
from letter import Letter, is_vowel, WordBreak, is_wordbreak, is_consonant, \
    simple_consonants_without_x, make_long, make_short, onsets
from cluster import ConsonantCluster
from misc import trace, dd, lazy, Pipeline, Multiple, run_multiple, \
    first_true, Incompatible, Unknown, flatten
from command_line import HasCommandLineStr
from testing import reduce_to_text


class Syllable(HasSource, HasCommandLineStr):
    """
    The elems of a Syllable are ConsonantClusters and vowels (Letters).
    """

    def __init__(self, *elems, source=None):
        self.elems = elems
        # ignore source: should derive the real source from the vowel in elems
        self.is_stressed = Unknown

    @property
    @lazy
    def vowel(self):
        return first_true(self.elems, is_vowel)
        
    @property
    @lazy
    def letters(self):
        return flatten(elem.letters for elem in self.elems)

    @property
    @lazy
    def clusters(self):
        return [
            elem
                for elem in self.elems
                    if isinstance(elem, ConsonantCluster)
        ]

    @property
    @lazy
    def is_open(self):
        for i in range(len(self.elems)):
            if is_vowel(self.elems[i]):
                break
        return i + 1 >= len(self.elems)

    @property
    @lazy
    def is_closed(self):
        return not self.is_open

    @property
    def could_be_heavy(self):
        return True

    @property
    def could_be_light(self):
        return self.is_open

    @property
    def could_be_heavy_or_light(self):
        return True

    @property
    def starts_with_consonant(self):
        return isinstance(self.elems[0], ConsonantCluster)

    @property
    @lazy
    def is_at_start_of_word(self):
        return self.elems[0].is_at_start_of_word

    @property
    @lazy
    def is_at_end_of_word(self):
        return self.elems[-1].is_at_end_of_word

    @property
    @lazy
    def starts_midword(self):
        return not self.elems[0].is_at_start_of_word

    @lazy
    def force_weight(self, weight):
        if weight == Heavy:
            return HeavySyllable(self)
        elif weight == Light:
            return LightSyllable(self)
        else:
            return self

    @property
    @lazy
    def word_instances(self):
        result = []
        for elem in self.elems:
            for w in elem.word_instances:
                if w not in result:
                    result.append(w)
        return result

    @property
    @lazy
    def without_source(self):
        return Syllable(*[cl.without_source for cl in self.elems])

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.elems == other.elems
        )

    def __hash__(self):
        return hash(tuple(self.elems))
        #TODO better hash

    @property
    @lazy
    def reduced_to_text(self):
        return Syllable(*[reduce_to_text(cl) for cl in self.elems])

    def __repr__(self):
        args = ', '.join(repr(elem) for elem in self.elems)
        if self.is_stressed == True:
            args = '(stressed) ' + args
        return '%s(%s)' % (self.__class__.__name__, args)

    def _make_str(self, f, tie, accent_f):
        result = ''
        prev_elem = None

        for elem in self.elems:
            if prev_elem is not None and elem.is_at_start_of_word:
                result += tie
            if self.is_stressed is True and is_vowel(elem):
                result += accent_f(f(elem))
            else:
                result += f(elem)
            prev_elem = elem
        return result

    def __str__(self):
        return self._make_str(
            str,
            '⁀',
            lambda x: x + "'"
        )

    def simon(self):
        return self._make_str(
            lambda x: x.simon(),
            '',
            lambda x: 'A(%s)' % x
        )

    def latex(self):
        return self._make_str(
            lambda x: x.latex(),
            r'{\tie}',
            lambda x: r"\'{%s}" % x
        )
#        result = ''
#        prev_elem = None
#
#        for elem in self.elems:
#            if elem.word_instance != prev_elem.word_instance:
#                result += 'r{\tie}'
#            result += elem.latex
#            prev_elem = elem
#
#        return result


class HeavySyllable(Syllable):

    is_heavy = True

    is_light = False

    def __init__(self, syllable, is_stressed=Unknown):
        self.base_syllable = syllable
        self.elems = [
            make_long(elem) if is_vowel(elem) and syllable.is_open else elem
                for elem in syllable.elems
        ]
        self.is_stressed = is_stressed

    def add_stress(self):
        if self.is_stressed == True:
            return self
        else:
            return HeavySyllable(self, is_stressed=True)


class LightSyllable(Syllable):
    
    is_heavy = False

    is_light = True

    def __init__(self, syllable, is_stressed=Unknown):
        self.base_syllable = syllable
        if syllable.is_closed:
            raise Incompatible
        self.elems = [
            elem if is_consonant(elem) else make_short(elem)
                for elem in syllable.elems
        ]
        self.is_stressed = is_stressed

    #TODO OAOO
    def add_stress(self):
        if self.is_stressed == True:
            return self
        else:
            return LightSyllable(self, is_stressed=True)


class Weight:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

Heavy = Weight('Heavy')
Light = Weight('Light')
HeavyOrLight = Weight('HeavyOrLight')


CC1 = TestVar('CC1', lambda x: isinstance(x, ConsonantCluster))
CC2 = TestVar('CC2', lambda x: isinstance(x, ConsonantCluster))
V1 = TestVar('V1', lambda x: is_vowel(x))
V2 = TestVar('V2', lambda x: is_vowel(x))

parse_syllables = CombinatoricMap(ignore_matched_input,
    (Var('SYLLABLE',
        Target(Optional(CC1), V1, Optional(CC2, NotFollowedBy(V2)))),
     ReplaceWith([Make(Syllable, Var('SYLLABLE'))]))
)

def midword_syllable_starts_without_onset(sy):
    onset = sy.elems[0]
    if is_vowel(onset):
        return False
    if not sy.starts_midword:
        return False
    return not onset.is_onset

MIDWORD_SYLLABLE_STARTS_WITHOUT_ONSET = \
    TestVar('MIDWORD_SYLLABLE_STARTS_WITHOUT_ONSET',
        midword_syllable_starts_without_onset
    )

remove_invalid_syllables = Filter(
    Disallow(MIDWORD_SYLLABLE_STARTS_WITHOUT_ONSET)
)


do_make_syllables = Pipeline(
    parse_syllables,
    remove_invalid_syllables
)

def make_syllables(with_clusterss):
    logging.info('SYLLABIFYING')
    return do_make_syllables(with_clusterss)
