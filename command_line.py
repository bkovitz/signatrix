# Command-line interface

import argparse
import sys
from abc import ABCMeta, abstractmethod

from misc import trace, dd, ObjectHolder, CommandLineError


options_parser = argparse.ArgumentParser(
    add_help=False
)
options_parser.add_argument(
    '--dbdir',
    nargs=1,
    type=str,
    default='db',
    help="database directory (default: db)"
)
scansion_group = options_parser.add_argument_group('scansion stages')
scansion_group.add_argument(
    '--letters',
    action='store_true',
    help='show all interpretations of the letters in each line'
)
scansion_group.add_argument(
    '--elisions',
    action='store_true',
    help='show stage in which elisions and hiatuses are added to each line'
)
scansion_group.add_argument(
    '--clusters',
    action='store_true',
    help='show stage in which line is broken into consonant clusters'
)
scansion_group.add_argument(
    '--syllables',
    action='store_true',
    help='show stage in which line is broken into syllables'
)
scansion_group.add_argument(
    '--feet',
    action='store_true',
    help='show final scans (included by default unless another scansion stage is chosen)'
)

options_parser.add_argument(
    '-l', '--line', '--lines',
    nargs=1,
    type=int,
    help="line number(s)",
    metavar='LINES'
)
options_parser.add_argument(
    '--known-words',
    nargs=1,
    type=str,
    help='exclude scans that violate word forms listed in FILENAME',
    metavar='FILENAME'
)
options_parser.add_argument(
    '--format',
    type=str,
    choices=['utf-8', 'latex', 'simon'],
    default='utf-8',
    help='output format; simon indicates short/long/accented vowels with S(),L(),A() (default: utf-8)'
)
options_parser.add_argument(
    '--original',
    action='store_true',
    help='original text rather than normalized text'
)

options_parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help="describe each stage as it starts"
)

command_line_parser = argparse.ArgumentParser(
    parents=[options_parser]
)
subparsers = command_line_parser.add_subparsers(
    title='commands', dest='command'
)

scan_parser = subparsers.add_parser(
    'scan',
    help='read text files and store scans into database',
    usage='%(prog)s [options] FILENAME [FILENAME]...',
    parents=[options_parser]
)
scan_parser.add_argument(
    'filename',
    type=str,
    help='text file to scan',
    metavar='FILENAME'
)

dump_parser = subparsers.add_parser(
    'dump',
    help='show database contents',
    usage='%(prog)s [options] DBNAME',
    parents=[options_parser]
)
dump_parser.add_argument(
    'dbname',
    type=str,
    help='name of database to dump'
)

tally_parser = subparsers.add_parser(
    'tally',
    help='tally word forms against scans',
    usage='%(prog)s [options] DBNAME [DBNAME]...',
    parents=[options_parser]
)
tally_parser.add_argument(
    'dbnames', type=str, nargs='+', help='names of databases to tally',
    metavar='DBNAME'
)

command_line_parser.usage = '\n' + ''.join(
    '  ' + p.format_usage()[7:]
        for p in [scan_parser, dump_parser, tally_parser]
)


# The globals that you want to import begin here.

def parse_command_line(argv=sys.argv):
    global command_line_arguments

    parsed = command_line_parser.parse_args(argv[1:])
    parsed.num_stages = sum(
        1
            for stage in [
                'letters', 'elisions', 'clusters', 'syllables', 'feet'
            ]
                if getattr(parsed, stage)
    )
    if parsed.num_stages == 0:
        parsed.feet == True
        parsed.num_stages = 1

    command_line_arguments.replace_with(parsed)
    if command_line_arguments.command is None:
        raise CommandLineError(
            '%s  %s --help' % (command_line_parser.format_usage(), sys.argv[0])
        )
    return command_line_arguments

# Initialized to defaults appropriate for unit testing. Override with real
# command-line arguments by calling parse_command_line.
command_line_arguments = ObjectHolder()
command_line_arguments.replace_with(
    parse_command_line(['testing-signatrix', 'scan', 'ignored'])
)


class HasCommandLineStr(metaclass=ABCMeta):

    @abstractmethod
    def latex(self):
        pass

    @abstractmethod
    def simon(self):
        pass

    def str_per_command_line(self):
        if command_line_arguments.format == 'latex':
            return self.latex()
        elif command_line_arguments.format == 'simon':
            return self.simon()
        else:
            return str(self)
