#command_line_parser = argparse.ArgumentParser(
#    description='Scan Latin verse and infer vowel quantities and accents.'
#)
#command_line_parser.add_argument(
#    '--scan', nargs='+', type=str, help='scan files and store in databases',
#        metavar='FILENAME'
#)
#command_line_parser.add_argument(
#    '--tally', nargs='+', type=str, help='tally word forms in databases',
#        metavar='DATABASE'
#)

class CommandLineError(RuntimeError):
    pass


def shortname(name):
    return splitext(basename(name))[0]

def pf(*args, **kwargs):
    print(*args, flush=True, **kwargs)

class CorpusDatabase:

    def __init__(self):
        self.work_by_name = {}

    def scan(self, dbname, workname):
        short_workname = shortname(workname)
        work = Work(short_workname)
        work.scan_file(open(workname, 'r'))
        with shelve.open(dbname) as f:
            f[work.name] = work

    def dump(self, dbfilename):
        with shelve.open(dbfilename, 'r') as f:
            for workname, work in f.items():
                for line in work.lines.values():
                    for scan in line.scans:
                        print(scan)
        
    def tally(self, dbfilenames, worknames=None):
        pf("reading works ", end="")
        for dbfilename in dbfilenames:
            with shelve.open(dbfilename, 'r') as f:
                pf("O", end="")
                for workname, work in f.items():
                    short_workname = shortname(workname) # FIXME: DCB  to read existing db file
                    self.work_by_name[short_workname] = work
                    pf(".", end="")
        pf("\n")
        dictionary = Dictionary()
        pf("tallying ", end="")
        for short_workname in (
            [shortname(w) for w in worknames] if worknames else
            self.work_by_name.keys()
            ):
            try:
                work = self.work_by_name[short_workname]
            except KeyError:
                raise CommandLineError('no such work: ' + short_workname)

            work = self.work_by_name[short_workname]
            pf("O", end="")
            for line in work.lines.values():
                pf(".", end="")
                for word_form in line.scans.word_forms:
                    dictionary.add_word_form(word_form, line)
            for word_form in dictionary.word_forms:
                for line in dictionary.lines_containing_word_form(word_form):
                    for word_instance in line.instances_of(
                        word_form.dictionary_word
                        ):
                        dictionary.add_scanset_proportion(
                            word_form,
                            line.scans.proportion_containing(
                                word_instance,
                                word_form
                            )
                        )
            pf("\n")
        dictionary.print_word_form_proportions()

def main(argv):
    #args = command_line_parser.parse_args(argv[1:])
    #print(args.scan)
    try:
        command, *args = argv
    except:
        raise CommandLineError('usage: command-line args')

    #dbname = 'signatrix.db'
    dbname = 'big.db'

    corpusdb = CorpusDatabase()
    if command == 'scan':
        for filename in args:
            corpusdb.scan(dbname, filename)
    elif command == 'dump':
        corpusdb.dump(dbname)
    elif command == 'tally':
        corpusdb.tally([dbname], args)
    else:
        raise CommandLineError("need a command: 'scan'")
