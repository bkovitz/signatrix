import logging

from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    CanMatchTargetElem, Disallow, TestVar, ignore_matched_input, \
    Make
from source import Source, HasSource
from letter import Letter, is_vowel, WordBreak, is_wordbreak
from command_line import HasCommandLineStr
from misc import trace, dd, lazy, Pipeline
from testing import reduce_to_text


class Elision(WordBreak, HasCommandLineStr):

    def __init__(self, *elided_letters, already_reduced=False):
        self.elided_letters = elided_letters
        self.already_reduced = already_reduced

    @property
    @lazy
    def word_instances(self):
        result = []
        for letter in self.elided_letters:
            for w in letter.word_instances:
                if w not in result:
                    result.append(w)
        return result

    @property
    @lazy
    def letters(self):
        return self.elided_letters

    @property
    def reduced_to_text(self):
        if self.already_reduced:
            return self
        else:
            return Elision(*[reduce_to_text(l) for l in self.elided_letters])

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.elided_letters == other.elided_letters
        )

    def __hash__(self):
        return hash(self.elided_letters)

    def __repr__(self):
        return 'Elision(%s)' % ', '.join(repr(l) for l in self.elided_letters)

    def __str__(self):
        return '(%s)' % ''.join(str(letter) for letter in self.letters)

    def simon(self):
        return 'E(%s)' % ''.join(letter.simon() for letter in self.letters)

    def latex(self):
        return '(%s)' % ''.join(letter.latex() for letter in self.letters)


class Hiatus(WordBreak, HasCommandLineStr):

    def __repr__(self):
        return 'Hiatus'

    @property
    def reduced_to_text(self):
        return self

    def __str__(self):
        return ''

    def simon(self):
        return '(H)'

    def latex(self):
        return ''

hiatus = Hiatus()


V1 = TestVar('V1', lambda l: is_vowel(l))
V2 = TestVar('V2', lambda l: is_vowel(l))
H = TestVar('H', lambda l: l.text == 'h')
M = TestVar('M', lambda l: l.text == 'm')
WB = TestVar('WB', is_wordbreak)
LETTER = TestVar('LETTER', lambda l: isinstance(l, Letter))
ANY = TestVar('ANY', lambda l: True)


generate_elisions = CombinatoricMap(
    ignore_matched_input,
    (Target(V1, WB, V2),
        ReplaceWith([Make(Elision, V1), V2], [V1, hiatus, V2])),
    (Target(V1, WB, H, V2),
        ReplaceWith([Make(Elision, V1, H), V2], [V1, hiatus, H, V2])),
    (Target(LETTER, V1, M, WB, V2),
        ReplaceWith(
            [LETTER, Make(Elision, V1, M), V2],
            [LETTER, V1, M, hiatus, V2])),
    (Target(LETTER, V1, M, WB, H, V2),
        ReplaceWith(
            [LETTER, Make(Elision, V1, M, H), V2],
            [LETTER, V1, M, hiatus, H, V2])),
    (Target(WB), ReplaceWith()),
    (Target(ANY), ReplaceWith([ANY]))
)

EH = TestVar('EH', lambda x: isinstance(x, (Elision, Hiatus)))

def add_hidden(letter, *hidden):
    return letter.add_hidden(*hidden)

hide_elisions_inside_letters = CombinatoricMap(
    ignore_matched_input,
    (Target(LETTER, EH),
        ReplaceWith([Make(add_hidden, LETTER, EH)])),
    (Target(ANY), ReplaceWith([ANY]))
)

do_make_elisions = Pipeline(
    generate_elisions,
    hide_elisions_inside_letters
)

def make_elisions(letterss):
    logging.info('ADDING ELISIONS')
    return do_make_elisions(letterss)
