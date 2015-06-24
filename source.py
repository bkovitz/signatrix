from abc import ABCMeta, abstractmethod

#from work import Work
from misc import dd, trace, lazy, isiterable


class Source:

    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def __eq__(self, other):
        return (
            isinstance(other, Source)
            and
            self.obj == other.obj
            and
            self.index == other.index
        )

    @lazy
    def __hash__(self):
        return hash(self.index)
        #TODO make a better hash

    def __repr__(self):
        return 'Source(%s, %s)' % (str(self.obj), str(self.index))


class HasSource(metaclass=ABCMeta):

    @abstractmethod
    def without_source(self):
        pass

    def whats_your(self, source_class):
        me = self
        while me.__class__ != source_class:
            try:
                me = me.source.obj
            except AttributeError:
                return None
        return me

    @property
    def work(self):
        import work
        return self.whats_your(work.Work)

    @property
    def line_num(self):
        return self.work.line_num


def force_source_from(obj):
    try:
        return obj.source
    except AttributeError:
        if type(obj) is str:
            return None
        elif isiterable(obj):
            try:
                return force_source_from(obj[0])
            except IndexError:
                return None
        else:
            return None
