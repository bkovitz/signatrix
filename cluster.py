from itertools import chain, product

from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    CanMatchTargetElem, Disallow, Filter, TestVar, ignore_matched_input, \
    Make, NotFollowedBy
from source import Source, HasSource, force_source_from
from letter import Letter, is_vowel, WordBreak, is_wordbreak, is_consonant, \
    onsets
from misc import trace, dd, lazy, Pipeline, Multiple, run_multiple
from testing import reduce_to_text


class ConsonantCluster(HasSource):

    def __init__(self, *letters):
        self.letters = letters

    @property
    def source(self):
        return force_source_from(self.letters[0])

    @property
    @lazy
    def without_source(self):
        return ConsonantCluster(*[l.without_source for l in self.letters])

    is_consonant = True

    is_vowel = False

    @property
    @lazy
    def is_at_start_of_word(self):
        return self.letters[0].is_at_start_of_word

    @property
    @lazy
    def is_at_end_of_word(self):
        return self.letters[-1].is_at_end_of_word

    @property
    @lazy
    def straddles_two_words(self):
        return (
            self.letters[0].word_instance is not self.letters[-1].word_instance
        )

    @property
    @lazy
    def is_onset(self):
        return self.text in onsets

    @property
    @lazy
    def word_instances(self):
        result = []
        for letter in self.letters:
            for w in letter.word_instances:
                if w not in result:
                    result.append(w)
        return result

    @property
    @lazy
    def text(self):
        return ''.join(letter.text for letter in self.letters)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.letters == other.letters
        )

    def __hash__(self):
        return hash(self.letters)

    @property
    @lazy
    def reduced_to_text(self):
        return ConsonantCluster(*[reduce_to_text(l) for l in self.letters])

    def __repr__(self):
        return 'ConsonantCluster(%s)' % ', '.join(repr(l) for l in self.letters)

    def __str__(self):
        result = ''
        prev_letter = None

        for letter in self.letters:
            if prev_letter is not None and letter.is_at_start_of_word:
                result += '⁀'
            result += str(letter)
            prev_letter = letter

        return result


@run_multiple
def group_into_clusters(letters):
    result = []
    while len(letters):
        chunk, letters = next_chunk(letters)
        if is_consonant(chunk[0]):
            result.append(divide_all_possible_ways(chunk))
        else:
            result.append([chunk])
    return Multiple(*[
        tuple(chain.from_iterable(elem))
            for elem in product(*result)
    ])

def divide_all_possible_ways(consonants):
    if len(consonants) == 1:
        return [[ConsonantCluster(consonants[0])]]
    else:
        result = [[ConsonantCluster(*consonants)]]
        for n in range(1, len(consonants)):
            result.append([
                ConsonantCluster(*consonants[0:n]),
                ConsonantCluster(*consonants[n:])
            ])
        return result

def next_chunk(letters):
    result = []
    while len(letters):
        letter = letters[0]
        if not is_consonant(letter):
            if len(result):
                return result, letters
            else:
                return [letter], letters[1:]
        else:
            result.append(letter)
            letters = letters[1:]
    return result, letters

CC = TestVar('CC', lambda x: isinstance(x, ConsonantCluster))
V = TestVar('V', lambda x: is_vowel(x))
CC_at_start_of_word = TestVar('CC_at_start_of_word',
    lambda x: isinstance(x, ConsonantCluster) and x.is_at_start_of_word
)
CC_at_end_of_word = TestVar('CC_at_end_of_word',
    lambda x: isinstance(x, ConsonantCluster) and x.is_at_end_of_word
)
NONONSET_at_end_of_word = TestVar('NONONSET_at_end_of_word',
    lambda x: (
        isinstance(x, ConsonantCluster)
        and
        x.is_at_end_of_word
        and
        x.text not in onsets
    )
)
NONONSET_STRADDLES_TWO_WORDS = TestVar('NONONSET_STRADDLES_TWO_WORDS',
    lambda x: (
        isinstance(x, ConsonantCluster)
        and
        x.straddles_two_words
        and
        x.text not in onsets
    )
)

remove_invalid_clusters = Filter(
    Disallow(CC_at_start_of_word, CC),
    Disallow(CC, CC_at_end_of_word, NotFollowedBy(V)),
    Disallow(NONONSET_at_end_of_word, V),
    Disallow(NONONSET_STRADDLES_TWO_WORDS)
)


make_clusters = Pipeline(
    group_into_clusters,
    remove_invalid_clusters
)
