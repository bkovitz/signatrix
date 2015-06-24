from letter import Letter
from source import Source
from misc import trace, dd, lazy


class WordInstance:

    def __init__(self, text, source):
        self.text = text
        self.source = source

    @property
    @lazy
    def to_letters(self):
        return [
            Letter(l, Source(self, index))
                for (index, l) in enumerate(self.text)
        ]

    def __eq__(self, other):
        return (
            isinstance(other, WordInstance)
            and
            self.text == other.text
            and
            self.source == other.source
        )

    def __hash__(self):
        return hash(self.text)
        #TODO make a better hash
        #return hash((self.text, self.source))

    def __repr__(self):
        return 'WordInstance(%s, %s)' % (repr(self.text), repr(self.source))

    def __str__(self):
        return repr(self.text)


class WordForm:

    def __init__(self, *letters):
        self.letters = tuple(letter.without_source() for letter in letters)
        self.dictionary_word = letters[0].dictionary_word

    def __hash__(self):
        return hash(self.letters)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and
            self.letters == other.letters
        )

    def __repr__(self):
        return 'WordForm(%s)' % ', '.join(repr(l) for l in self.letters)

    def __str__(self):
        return ''.join(str(l) for l in self.letters)
