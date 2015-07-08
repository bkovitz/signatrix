from collections import defaultdict
from statistics import mean

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


