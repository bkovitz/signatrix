from source import Source
from line import Line
from misc import lazy, trace, dd, Multiple

class Book:

    def __init__(self, name=''):
        self.name = name
        self.d = {}  # line_num: Line

    def __getitem__(self, line_num):
        return self.d[line_num]

    def __setitem__(self, line_num, line):
        self.d[line_num] = line
        return line

    def __delitem__(self, line_num):
        del self.d[line_num]

    def __iter__(self):
        return iter(self.d)

    def __contains__(self, line_num):
        return line_num in self.d

    @property
    def lines(self):
        for line_num in sorted(self.d.keys()):
            yield self.d[line_num]


def scan_book(name, file):
    line_num = 0
    book = Book(name)
    for line_string in file:
        line_string = line_string.strip()
        if line_string:
            line_num += 1
            if line_num not in book:
                line = Line(line_string, Source(book, line_num))
                book[line_num] = line
                print('%d. %s (%d scans)' % (
                    line_num,
                    line.text,
                    len(line.scans)
                ))
    return book
