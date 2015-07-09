import re
import logging

#from list import *
from source import Source, HasSource
from word import WordInstance
from letter import Letter, make_letters
from elision import make_elisions
from cluster import make_clusters
from syllable import make_syllables
from scan import make_scans, eliminate_redundant_scans
from command_line import command_line_arguments
from misc import lazy, trace, dd, Multiple, number_strs, flatten, intersperse, \
    flatstr, str_per_command_line


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
        return eliminate_redundant_scans(make_scans(self.syllables))

    def __repr__(self):
        return 'Line'
        #TODO Add short version of index and source.

    @property
    @lazy
    def line_num_str(self):
        try:
            return '%d. ' % self.source.index
        except AttributeError:
            return ''

    def __str__(self):
        result = []
        if self.source:
            result.append('%d. %s' % (self.source.index, self.original_text))
        else:
            result.append(self.original_text)
        if len(self.scans):
            for scan in self.scans:
                result.append('  %s' % str(scan))
        else:
            result.append('  (Failed to scan.)')
        return '\n'.join(result)

    def str_per_command_line(self):
        result = []

        #result.append(self.text_per_command_line())
        text_item = []
        if command_line_arguments.original:
            text_item.append(self.line_num_str + self.original_text)
        if command_line_arguments.text:
            text_item.append(self.line_num_str + self.text)
        result.append('\n'.join(text_item))

        if command_line_arguments.letters:
            result.append(str_per_command_line(self.letters))
        if command_line_arguments.elisions:
            result.append(str_per_command_line(self.with_elisions))
        if command_line_arguments.clusters:
            result.append(str_per_command_line(self.with_clusters))
        if command_line_arguments.syllables:
            result.append(str_per_command_line(self.syllables))
        if command_line_arguments.feet:
            result.append(str_per_command_line(self.scans))
        return '\n'.join(intersperse('', result))

    def text_per_command_line(self):
        return self.line_num_str() + (
            self.original_text
                if command_line_arguments.original
                else self.text
        )
        

