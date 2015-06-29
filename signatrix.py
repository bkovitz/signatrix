# Command-line interface to signatrix, the Latin-scansion program.

import argparse
import shelve
from collections import defaultdict
from statistics import mean
from os.path import basename, splitext
import sys

from work import Work
from book import Book, scan_book, BookDatabase
from misc import trace, dd, SignatrixError


class Tally:

    def __init__(self):
        self.word_form_to_lines = defaultdict(set)
        self.word_form_to_scanset_proportion = defaultdict(list)
        self.dictionary_word_to_word_forms = defaultdict(set)
        self.dictionary_word_to_lines = defaultdict(set)
        self.num_instances = defaultdict(int) # dict_word: int
        self.num_scans = defaultdict(int)     # dict_word: int

    def add_word_form(self, word_form, line):
        dict_word = word_form.dictionary_word
        self.word_form_to_lines[word_form].add(line)
        self.dictionary_word_to_word_forms[dict_word].add(word_form)
        if line not in self.lines_containing_dictionary_word(dict_word):
            self.num_instances[dict_word] += len(line.instances_of(dict_word))
            self.num_scans[dict_word] = \
                self.num_instances[dict_word] * len(line.scans)
            self.dictionary_word_to_lines[dict_word].add(line)

    @property
    def word_forms(self):
        return self.word_form_to_lines.keys()

    def lines_containing_word_form(self, word_form):
        return self.word_form_to_lines[word_form]

    def lines_containing_dictionary_word(self, dict_word):
        return self.dictionary_word_to_lines[dict_word]

    def add_scanset_proportion(self, word_form, proportion):
        self.word_form_to_scanset_proportion[word_form].append(proportion)

    @property
    def dictionary_words(self):
        return sorted(set([
            word_form.dictionary_word for word_form in self.word_forms
        ]))

    def record_all_word_forms(self, lines):
        for line in lines:
            for word_form in line.scans.word_forms:
                self.add_word_form(word_form, line)

    def count_word_form_proportions(self):
        for dict_word in self.dictionary_words:
            for line in self.lines_containing_dictionary_word(dict_word):
                for word_instance in line.instances_of(dict_word):
                    for word_form in \
                            self.dictionary_word_to_word_forms[dict_word]:
                          self.add_scanset_proportion(
                              word_form,
                              line.scans.proportion_containing(
                                  word_instance,
                                  word_form
                              )
                          )

    def print_word_form_proportions(self):
        for dict_word in self.dictionary_words:
            print('%s (occurrences: %d, scans: %d)' % (
                dict_word,
                self.num_instances[dict_word],
                self.num_scans[dict_word]
            ))
            for word_form in self.dictionary_word_to_word_forms[dict_word]:
                print("  %s %3.4f" % (str(word_form),
                  mean(self.word_form_to_scanset_proportion[word_form])))


def scan(filename):
    return scan_book(book_name(filename), open(filename, 'r'))
#    with shelve.open(database_name(filename)) as sh:
#        sh[book.name] = book

def dump(dbname):
    for line in BookDatabase(dbname).lines:
        print(line)

def tally(dbnames):
    tally = Tally()
#     for dbname in dbnames:
#         with shelve.open(dbname, 'r') as sh:
#             for book_name in sh.keys():
#                 book = sh[book_name]
#                 tally.record_all_word_forms(book.lines)
    for dbname in dbnames:
        tally.record_all_word_forms(BookDatabase(dbname).lines)
    tally.count_word_form_proportions()
    tally.print_word_form_proportions()


def book_name(filename):
    return splitext(basename(filename))[0]

def database_name(filename):
    return book_name(filename) + '.db'


class Main:

    def __init__(self, argv):
        if len(argv) < 2:
            self.usage()
        elif argv[1] == 'scan':
            if not argv[2:]:
                self.usage()
            for filename in argv[2:]:
                scan(filename)
        elif argv[1] == 'dump':
            if not argv[2:]:
                self.usage()
            for filename in argv[2:]:
                dump(filename)
        elif argv[1] == 'tally':
            if not argv[2:]:
                self.usage()
            tally(argv[2:])
        else:
            self.usage()

    @classmethod
    def usage(cls):
        print(
'''usage:
  signatrix scan filenames...
  signatrix dump databases...
  signatrix tally databases...''', file=sys.stderr,)
        sys.exit(2)


if __name__ == '__main__':
    import sys
    try:
        Main(sys.argv)
    except (SignatrixError, IOError) as exc:
        print(exc)
        sys.exit(1)
