from collections import defaultdict
import itertools

from replace import CombinatoricMap, Target, ReplaceWith, Var, Any, MakeInto, \
    CanMatchTargetElem, Disallow, Filter, TestVar, ignore_matched_input, \
    Make, Optional, NotFollowedBy, Match, ChunkResult, ParseInto, Or, Chunk
from source import Source, HasSource, force_source_from
from letter import Letter, is_vowel, WordBreak, is_wordbreak, is_consonant, \
    simple_consonants_without_x, is_onset, is_midword_coda
from cluster import ConsonantCluster
from syllable import Heavy, Light, HeavyOrLight
from misc import trace, dd, lazy, Pipeline, Multiple, run_multiple, \
    Incompatible, flatten, Unknown
from word import WordForm
from testing import reduce_to_text

class SyllableMap:

    @classmethod
    def make_map(cls, word_instances, syllables):
        result = defaultdict(list)
        for word in word_instances:
            result[word] += [
                sy
                    for sy in syllables
                        if sy.vowel.word_instance == word
        ]
        return result

    def __init__(self, word_instances, syllables):
        self.word_to_syllables = self.make_map(word_instances, syllables)
        
    def is_stressed(self, syllable):
        word_instance = syllable.vowel.word_instance
        syllables = self.word_to_syllables[word_instance]
        num_syllables = len(syllables)
        if num_syllables == 1:
            return False
        elif num_syllables == 2:
            return syllable == syllables[0]
        elif syllable == syllables[-2]:  # penult
            return syllables[-2].is_heavy == True
        elif syllable == syllables[-3]:  # antepenult
            return syllables[-2].is_light == True
        else:
            return False


class Scan:

    def __init__(self, *raw_feet):
        # Here, "raw" means "We don't yet know which syllables are stressed."
        self.raw_feet = raw_feet
        raw_syllable_map = SyllableMap(
            self._word_instances(self.raw_feet),
            flatten(foot.syllables for foot in raw_feet)
        )
        self.feet = [
            foot.add_stresses(raw_syllable_map) for foot in self.raw_feet
        ]

    def __iter__(self):
        return iter(self.feet)

    @classmethod
    @lazy
    def _word_instances(cls, raw_feet):
        result = []
        for foot in raw_feet:
            for w in foot.word_instances:
                if w not in result:
                    result.append(w)
        return result

    #TODO OAOO?
    @property
    @lazy
    def word_instances(self):
        return self._word_instances(self.raw_feet)

    @lazy
    def form_of(self, word_instance):
        index = self.word_instances.index(word_instance)
        return self.word_form_list[index]

    @property
    @lazy
    def syllables(self):
        return flatten(foot.syllables for foot in self.feet)

    @property
    @lazy
    def letters(self):
        return flatten(foot.letters for foot in self.feet)

    @property
    @lazy
    def word_form_list(self):
        result = []
        for word, letters in itertools.groupby(
            self.letters,
            lambda letter: letter.word_instance.text
        ):
            result.append(WordForm(*letters))
        return result
        
    @property
    @lazy
    def word_forms(self):
        return frozenset(self.word_form_list)

    @property
    @lazy
    def clusters(self):
        return flatten(sy.clusters for sy in self.syllables)

    @property
    @lazy
    def syllable_map(self):
        return SyllableMap(self._word_instances(self.raw_feet), self.syllables)

    @property
    @lazy
    def score_by_onsets_and_codas(self):
        score = 0
        for sy in self.syllables:
            if is_vowel(sy.elems[0]):
                score += 1
            elif is_onset(sy.elems[0]):
                score += 1

            if len(sy.elems) == 1:
                continue
            
            if is_consonant(sy.elems[-1]):
                if is_midword_coda(sy.elems[-1]):
                    score += 1
        return score

    @property
    def foot_types(self):
        return [foot.__class__ for foot in self.feet]

    def __repr__(self):
        return 'Scan(%s)' % ', '.join(repr(foot) for foot in self.feet)

    def __str__(self):
        return '/'.join(str(foot) for foot in self.feet).strip()

    def latex(self):
        return str(self)


class Scanset:

    def __init__(self, *scans):
        self.scans = scans

    def __iter__(self):
        return iter(self.scans)

    def __getitem__(self, index):
        return self.scans[index]

    def __len__(self):
        return len(self.scans)

    @property
    @lazy
    def word_forms(self):
        return frozenset().union(*(scan.word_forms for scan in self.scans))

    @lazy
    def proportion_containing(self, word_instance, word_form):
        count = sum(
            1
                for scan in self.scans
                    if scan.form_of(word_instance) == word_form
        )
        return float(count) / len(self.scans)


class Foot(Chunk):

    # Subclass must defined 'weights' member: list of required Syllable
    # attributes.

    def __init__(self, *raw_syllables, weights_are_already_known=False):
        if not weights_are_already_known:
            self.raw_syllables = raw_syllables
            self.syllables = [
                self.raw_syllables[i].force_weight(self.weights[i])
                    for i in range(len(self.raw_syllables))
            ]
        else:
            self.syllables = self.raw_syllables = raw_syllables

    @classmethod
    def match_and_replace(cls, x, env):
        l = len(cls.weights)
        if len(x) < l:
            return []
        try:
            foot = cls(*x[:l])
        except Incompatible:
            return []
        return [
            ChunkResult([foot], x[l:], env)
        ]

    #TODO Subclass FootWithKnownStress?
    def add_stresses(self, syllable_map):
        return self.__class__(*(
            sy.add_stress() if syllable_map.is_stressed(sy) else sy
                for sy in self.syllables
        ), weights_are_already_known=True)

    @property
    @lazy
    def word_instances(self):
        result = []
        for sy in self.syllables:
            for w in sy.word_instances:
                if w not in result:
                    result.append(w)
        return result

    @property
    @lazy
    def letters(self):
        return flatten(sy.letters for sy in self.syllables)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.raw_syllables == other.raw_syllables
        )

    def __hash__(self):
        return hash(tuple(self.syllables))
        #@TODO better hash

    @property
    @lazy
    def reduced_to_text(self):
        return self.__class__(
            *[reduce_to_text(sy) for sy in self.raw_syllables]
        )

    def __repr__(self):
        return self.__class__.__name__ + \
            '(%s)' % ', '.join(repr(sy) for sy in self.raw_syllables)

    def __str__(self):
        result = ''
        for sy in self.syllables:
            if sy.is_at_start_of_word:
                result += ' '
            else:
                result += '-'
            result += str(sy)
        if not sy.is_at_end_of_word:
            result += '-'
        else:
            result += ' '
        return result


class Dactyl(Foot):
    weights = [Heavy, Light, Light]

class Spondee(Foot):
    weights = [Heavy, Heavy]

class TailSpondee(Foot):
    weights = [Heavy, HeavyOrLight]


hexameter = ParseInto(
    Or(Dactyl, Spondee),
    Or(Dactyl, Spondee),
    Or(Dactyl, Spondee),
    Or(Dactyl, Spondee),
    Dactyl,
    TailSpondee
)


@run_multiple
def make_scans(syllables, parser=hexameter):
    return Multiple(*(Scan(*parse) for parse in parser(syllables)))

def eliminate_redundant_scans(scans):
    equivalent_scans = defaultdict(list)  # tuple(Letters): list(scans)
    for scan in scans:
        equivalent_scans[tuple(scan.letters)].append(scan)
    #dd('EQ', list(equivalent_scans.values())[0])
    #dd('BEST', str(best_scan(equivalent_scans[0])))
    #return Scanset(*(
        #eqs[0] if len(eqs) == 1 else best_scan(eqs)
            #for eqs in equivalent_scans.values()
    #))
    result = [
        eqs[0] if len(eqs) == 1 else best_scan(eqs)
            for eqs in equivalent_scans.values()
    ]
    assert len([x for x in result if isinstance(x, tuple)]) == 0
    return Scanset(*result)

def best_scan(scans):
    return sorted(
        scans,
        key=lambda scan: scan.score_by_onsets_and_codas,
        reverse=True
    )[0]

