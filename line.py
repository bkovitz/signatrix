import re

#from list import *
from source import Source, HasSource
from word import WordInstance
from letter import Letter, make_letters
from elision import make_elisions
from cluster import make_clusters
from syllable import make_syllables
from scan import make_scans, eliminate_redundant_scans
from misc import lazy, trace, dd, Multiple


alpha_only = re.compile('[^ a-z]')

def remove_spaces_and_nonalphabetics(s):
    return ' '.join(alpha_only.sub('', s.lower()).split())


class Line(HasSource):

    def __init__(self, original_text, source=None):
        self.original_text = original_text
        self.text = remove_spaces_and_nonalphabetics(self.original_text)
        self.source = source

    @property
    @lazy
    def word_instances(self):
        return tuple(
            WordInstance(w, Source(self, index))
                for index, w in enumerate(self.text.split())
        )

    @lazy
    def instances_of(self, dictionary_word):
        return [
            wi
                for wi in self.word_instances
                    if wi.text == dictionary_word
        ]

    def without_source(self):
        return Line(self.original_text)

    @property
    @lazy
    def letters(self):
        return make_letters(self.word_instances)

    @property
    @lazy
    def with_elisions(self):
        return make_elisions(self.letters)

    @property
    @lazy
    def with_clusters(self):
        return make_clusters(self.with_elisions)

    @property
    @lazy
    def syllables(self):
        return make_syllables(self.with_clusters)

    @property
    @lazy
    def scans(self):
        #return make_scans(self.syllables)
        return eliminate_redundant_scans(make_scans(self.syllables))

    def __repr__(self):
        return 'Line'
        #TODO Add short version of index and source.

    def __str__(self):
        result = []
        if self.source:
            result.append('%d. %s' % (self.source.index, self.original_text))
        else:
            result.append(self.original_text)
        for scan in self.scans:
            result.append('  %s' % str(scan))
        return '\n'.join(result)


