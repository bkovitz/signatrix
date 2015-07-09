# Signatrix, the Latin-scansion program.

from collections import defaultdict
from os.path import basename, splitext
import sys
import logging

from work import Work
from book import Book, scan_book, BookDatabase
from misc import trace, dd, SignatrixError, CommandLineError
from command_line import parse_command_line, command_line_arguments


def scan(filename):
    return scan_book(book_name(filename), open(filename, 'r'))

def dump(dbname):
    for line in BookDatabase(dbname, flag='r').lines:
        print(line.str_per_command_line())
        if command_line_arguments.num_stages > 0:
            print()
            if command_line_arguments.num_stages > 1:
                print()

def tally(dbnames):
    tally = Tally()
    for dbname in dbnames:
        tally.record_all_word_forms(BookDatabase(dbname).lines)
    tally.count_word_form_proportions()
    tally.print_word_form_proportions()


def book_name(filename):
    return splitext(basename(filename))[0]

def database_name(filename):
    return book_name(filename) + '.db'


def main(argv):
    parse_command_line(argv)

    logging.basicConfig(
        format='%(message)s',
        level=(
            logging.INFO if command_line_arguments.verbose else logging.WARNING
        )
    )

    command = command_line_arguments.command
    if command == 'scan':
        scan(command_line_arguments.filename)
    elif command == 'dump':
        dump(command_line_arguments.dbname)
    elif command == 'tally':
        tally(command_line_arguments.dbnames)
    else:
        raise SignatrixError('unrecognized command: ' + command)


if __name__ == '__main__':
    import sys
    try:
        main(sys.argv)
    except CommandLineError as exc:
        print(exc)
        sys.exit(2)
    except (SignatrixError, IOError, OSError, KeyboardInterrupt) as exc:
        print(exc)
        sys.exit(1)

