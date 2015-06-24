from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    CanMatchTargetElem, Disallow, Filter, TestVar
from source import Source, HasSource
from misc import trace, dd, lazy, Pipeline, flatten, intersperse, \
    run_multiple, Multiple, Unknown, Incompatible


class Letter(CanMatchTargetElem, HasSource):

    unicode_table = {}

    digraph_unicode_table = {
        'ae': 'æ',
        'oe': 'œ'
    }

#    latex_table = {}
#
#    digraph_latex_table = {
#        'ae': r'{\ae}',
#        'oe': r'{\oe}'
#    }

    def __init__(self, text, source=None, hidden=()):
        self.text = text
        self.source = source
        self.hidden = hidden
        # Subclass to appropriate Vowel class unless we already are a Vowel.
        if is_vowel(self.text) and not isinstance(self, Vowel):
            self.__class__ = self.default_vowel_class(self.text)

    @classmethod
    def default_vowel_class(cls, text):
        if len(text) > 1:
            return LongVowel
        else:
            return Vowel

    def add_hidden(self, *hidden):
        return self.__class__(
            self.text, self.source, hidden=(self.hidden + hidden)
        )

    @property
    @lazy
    def letters(self):
        return [self]

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and
            self.text == other.text
            and
            self.source == other.source
            and
            self.hidden == other.hidden
        )

    def matches_target_elem(self, target_elem):
        return self.text == target_elem

    def without_source(self):
        if self.source is None:
            return self
        else:
            return self.__class__(self.text, source=None, hidden=self.hidden)

    @property
    @lazy
    def is_consonant(self):
        return self.text[0] in simple_consonants

    @property
    @lazy
    def is_vowel(self):
        return self.text[0] in simple_vowels

    is_wordbreak = False

    @property
    @lazy
    def is_at_start_of_word(self):
        if self.source is None:
            return False
        else:
            return self.source.index == 0

    @property
    @lazy
    def is_at_end_of_word(self):
        if self.source is None:
            return False
        else:
            return (
                self.source.index + len(self.text) >=
                    len(self.word_instance.text)
            )

    @property
    @lazy
    def word_instance(self):
        if self.source:
            return self.source.obj
            #TODO Verify that the source is a WordInstance
        else:
            return None

    @property
    @lazy
    def dictionary_word(self):
        try:
            return self.word_instance.text
        except AttributeError:
            return None

    @property
    @lazy
    def word_instances(self):
        return [self.word_instance]

    def __hash__(self):
        #return hash((self.text, self.source))
        return hash((self.__class__, self.text,))

    def __repr__(self):
        if self.source is None:
            return '%s(%s)' % (self.__class__.__name__, repr(self.text))
        else:
            return '%s(%s, %s)' % (
                self.__class__.__name__,
                repr(self.text),
                repr(self.source)
            )

    @lazy
    def __str__(self):
        return (
            self.make_unicode(self.text)
            +
            ''.join(str(h) for h in self.hidden)
        )

    @classmethod
    def make_unicode(cls, text):
        try:
            return cls.unicode_table[text]
        except KeyError:
            try:
                return cls.digraph_unicode_table[text]
            except KeyError:
                return text
        
    def latex(self):
        return str(self)


class Vowel(Letter):

    is_long = Unknown

    is_onset = False

    @property
    def is_short(self):
        return not self.is_long

#    def make_short(self):
#        return ShortVowel(self)
#
#    def make_long(self):
#        return LongVowel(self)

    def make_long(self):
        return LongVowel(self.text, self.source, self.hidden)

    def make_short(self):
        return ShortVowel(self.text, self.source, self.hidden)


class LongVowel(Vowel):

    unicode_table = {
        'a': 'ā',
        'e': 'ē',
        'i': 'ī',
        'o': 'ō',
        'u': 'ū'
    }

    #def __init__(self, vowel, hidden=[]):
        #super().__init__(vowel.text, vowel.source, hidden=hidden)

    is_long = True

    def make_short(self):
        raise Incompatible

    def make_long(self):
        return self


class ShortVowel(Vowel):
    
    unicode_table = {
        'a': 'ă',
        'e': 'ĕ',
        'i': 'ĭ',
        'o': 'ŏ',
        'u': 'ŭ'
    }

    #def __init__(self, vowel, hidden=[]):
        #super().__init__(vowel.text, vowel.source, hidden=hidden)

    is_long = False

    def make_short(self):
        return self

    def make_long(self):
        raise Incompatible


def make_long(x):
    if isinstance(x, Vowel):
        return x.make_long()
    else:
        return x

def make_short(x):
    if isinstance(x, Vowel):
        return x.make_short()
    else:
        return x


class WordBreak(CanMatchTargetElem):

    def matches_target_elem(self, target_elem):
        return target_elem.isspace()

    text = ' '

    is_consonant = False

    is_wordbreak = True

    def __repr__(self):
        return 'WordBreak'


wordBreak = WordBreak()

simple_consonants = frozenset(list('bcdfghjklmnpqrstvxz') + ['qu'])
simple_consonants_without_x = simple_consonants - frozenset(['x'])
simple_consonants_without_j = simple_consonants - frozenset(['j'])
simple_vowels = frozenset('aeiouy')

onsets = simple_consonants_without_x | frozenset([
    'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gv',
    'pl', 'pr', 'scl', 'scr', 'sc', 'sl', 'spl', 'spr', 'sp',
    'str', 'st', 'squ', 'tr'
])

midword_codas = simple_consonants_without_j

def is_consonant(x):
    try:
        return x.is_consonant
    except AttributeError:
        if type(x) is str and len(x):
            return x[0] in simple_consonants
        else:
            return False

def is_vowel(x):
    try:
        return x.is_vowel
    except AttributeError:
        if type(x) is str and len(x):
            return x[0] in simple_vowels
        else:
            return False

def is_onset(x):
    try:
        return x.text in onsets
    except AttributeError:
        return x in onsets

def is_midword_coda(x):
    try:
        return x.text in midword_codas
    except AttributeError:
        return x in midword_codas

def is_wordbreak(x):
    if type(x) is str:
        return x.isspace()
    else:
        return x.is_wordbreak

def make_into_letter(rw_object, source):
    if isinstance(rw_object, Letter):
        return rw_object
    elif isinstance(rw_object, WordBreak):
        return rw_object
    elif rw_object == ' ':
        return wordBreak
    else:
        return Letter(rw_object, source)


C = TestVar('C', is_consonant)
V = TestVar('C', is_vowel)
WB = TestVar('WB', is_wordbreak)

def word_instances_to_letters(word_instances):
    return [wordBreak] + flatten(
        intersperse([' '], [w.to_letters for w in word_instances])
    ) + [wordBreak]

ij_uv = CombinatoricMap(
    make_into_letter,
    (Target('q', 'u'), ReplaceWith(['qu'])),
    (Target('q', 'v'), ReplaceWith(['qu'])),
    (Target('i'), ReplaceWith(['i'], ['j'])),
    (Target('j'), ReplaceWith(['i'], ['j'])),
    (Target('u'), ReplaceWith(['u'], ['v'])),
    (Target('v'), ReplaceWith(['u'], ['v'])),
    (Target(Var('A', Any)), ReplaceWith([Var('A')]))
)

digraphs = CombinatoricMap(
    make_into_letter,
    (Target('a', 'e'), ReplaceWith(['ae'], ['a', 'e'])),
    (Target('a', 'u'), ReplaceWith(['au'], ['a', 'u'])),
    (Target('c', 'h'), ReplaceWith(['ch'])),
    (Target('p', 'h'), ReplaceWith(['ph'])),
    (Target('r', 'h'), ReplaceWith(['rh'])),
    (Target('e', 'u'), ReplaceWith(['eu'], ['e', 'u'])),
    (Target('o', 'e'), ReplaceWith(['oe'], ['o', 'e'])),
    (Target('u', 'j'), ReplaceWith(['uj'])),
    (Target(Var('A', Any)), ReplaceWith([Var('A')]))
)

remove_invalid_letter_combinations = Filter(
    Disallow('v', C),
    Disallow('j', C),
    Disallow('uj', C),
    Disallow(WB, 'uj'),
    Disallow(WB, 'u', 'j'),
    Disallow(C, 'v', WB),
    Disallow(C, 'j', WB),
    Disallow('i', 'j', WB),
    Disallow(WB, 'u', V),
    Disallow('v', C),
    Disallow('j', C),
    Disallow('c', 'v')
)

@run_multiple
def strip_leading_and_trailing_wordbreaks(letters):
    return Multiple(letters[1:-1])

make_letters = Pipeline(
    word_instances_to_letters,
    ij_uv,
    digraphs,
    remove_invalid_letter_combinations,
    strip_leading_and_trailing_wordbreaks
)
