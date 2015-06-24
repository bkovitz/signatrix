from source import Source
from line import Line
from misc import lazy, trace, dd, Multiple

class Work:

    def __init__(self, name=''):
        self.name = name
        self.line_num = 0
        self.lines = {}  # line_num: Line
        
    def file_iter(self, file):
        def generator():
            for line_string in file:
                line_string = line_string.strip()
                if line_string:
                    self.line_num += 1
                    line = Line(line_string, Source(self, self.line_num))
                    self.lines[self.line_num] = line
                    print('%d. %s (%d scans)' % (
                        self.line_num,
                        line.text,
                        len(line.scans)
                    ))
                    yield line

        return generator()

    def scan_file(self, file):
        list(self.scans_strings(file))

    def scans_strings(self, file):
        for line in self.file_iter(file):
            for scan in line.scans:
                yield str(scan)
            yield('')
