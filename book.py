from sys import stdout
from os.path import basename, splitext
import shelve
import dbm

from source import Source
from line import Line
from misc import lazy, trace, dd, Multiple, strip_white_space, safe_mkdir
from command_line import command_line_arguments

# class Book:
# 
#     def __init__(self, name=''):
#         self.name = name
#         self.d = {}  # line_num: Line
# 
#     def __getitem__(self, line_num):
#         return self.d[line_num]
# 
#     def __setitem__(self, line_num, line):
#         self.d[line_num] = line
#         return line
# 
#     def __delitem__(self, line_num):
#         del self.d[line_num]
# 
#     def __iter__(self):
#         return iter(self.d)
# 
#     def __contains__(self, line_num):
#         return line_num in self.d
# 
#     @property
#     def lines(self):
#         for line_num in sorted(self.d.keys()):
#             yield self.d[line_num]


class Book:

    def __init__(self, name):
        self.name = name

    def __eq_(self, other):
        return (
            isinstance(other, Book)
            and
            self.name == other.name
        )

    def __repr__(self):
        return 'Book(%s)' % repr(self.name)


class BookDatabase:

    @classmethod
    def database_name(cls, filename):
        return 'db/' + strip_white_space(cls.book_name(filename)) #+ '.db'

    @classmethod
    def book_name(cls, filename):
        return splitext(basename(filename))[0]

    def __init__(self, book, dbname=None, flag='c'):
        if type(book) is str:
            book = Book(book)
        self.book = book
        self.name = book.name
        if dbname is None:
            self.dbname = self.database_name(self.name)
        else:
            self.dbname = dbname
        safe_mkdir(command_line_arguments.dbdir)
        try:
            self.sh = shelve.open(self.dbname, flag=flag)
        except dbm.error as exc:
            # HACK: shelve seems to offer no way to tell that a db file
            # doesn't exist, even when passed flag='r'.
            if exc.args == ("need 'c' or 'n' flag to open new db",):
                raise OSError('database not found: ' + self.dbname)
            else:
                raise

    def __del__(self):
        try:
            self.sh.close()
        except AttributeError:
            pass

    def __setitem__(self, line_num, line):
        self.sh[str(line_num)] = line
        return line

    def __getitem__(self, line_num):
        return self.sh[str(line_num)]

    def __delitem__(self, line_num):
        del self.sh[str(line_num)]

    def __iter__(self):
        return iter(self.sh)

    def __contains__(self, line_num):
        return str(line_num) in self.sh.keys()

    def __len__(self):
        return len(self.sh)

    @property
    def lines(self):
        for line_num in sorted(self.sh.keys(), key=int):
            # DEBUG
            o = self.sh[line_num]

            yield self.sh[line_num]


def scan_book(name, from_file, output=stdout):
    line_num = 0
    book = Book(name)
    bookdb = BookDatabase(book)
    for line_string in from_file:
        line_string = line_string.strip()
        if line_string:
            line_num += 1
            if line_num not in bookdb:
                line = Line(line_string, Source(book, line_num))
                bookdb[line_num] = line
                print('%d. %s (%d scans)' % (
                    line_num,
                    line.text_per_command_line(),
                    len(line.scans)
                ), file=output)
                output.flush()
    return bookdb

