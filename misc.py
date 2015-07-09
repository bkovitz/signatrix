import functools
from itertools import islice, chain, repeat, tee, filterfalse
import types
import collections
import os
import re


class SignatrixError(RuntimeError): pass

class CommandLineError(SignatrixError): pass


trace_indent = 0

def indent():
    return ' ' * trace_indent

def trace(func, name=None):
    def tr(*args, **kwargs):
        global trace_indent
        print(
            '%s%s(%s)'
            %
            (
                ' ' * trace_indent,
                func.__name__ if name is None else name,
                ', '.join(repr(arg) for arg in args)
                +
                ', '.join(
                    '%s=%s' % (kwarg[0], repr(kwarg[1]))
                        for kwarg in kwargs.items()
                )
            )
        )
        trace_indent += 2
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            trace_indent -= 2
            print('%s%s %s' % (indent(), 'raised', repr(e)))
            raise
        else:
            trace_indent -= 2
            if isinstance(result, types.GeneratorType):
                is_generator = True
                result = list(result)
                result_str = 'generator(%s)' % repr(result)
            else:
                is_generator = False
                result_str = repr(result)
            print('%sreturned %s' % (
                indent(),
                result_str
            ))
#            if is_generator:
#                yield_all_items(result)
#                for item in result:
#                    yield item
#            else:
            return result

    return tr

def dd(*items):
    """Display for debugging. Like print(), but indents along with @trace."""
    print('%s%s' % (indent(), ', '.join(repr(item) for item in items)))
    return items


class ClassUnknown:

    def __repr__(self):
        return 'Unknown'

Unknown = ClassUnknown()


class Incompatible(Exception):
    pass


class Multiple(tuple):
    """
    A Multiple holds multiple results, like what most stages of scansion
    generate.
    """

    def __new__(cls, *elems):
        return super().__new__(cls, elems)

    def __repr__(self):
        if not len(self):
            return '%s()' % self.__class__.__name__
        else:
            global trace_indent
            trace_indent += 2
            result = '%s(\n%s\n)' % (
                self.__class__.__name__,
                ',\n'.join('%s%s' % (indent(), repr(x)) for x in self)
            )
            trace_indent -= 2
            return result

    def __str__(self):
        if not len(self):
            return '%s()' % self.__class__.__name__
        else:
            global trace_indent
            trace_indent += 2
            result = '%s(\n%s\n)' % (
                self.__class__.__name__,
                ',\n'.join('%s%s' % (indent(), flatstr(x)) for x in self)
            )
            trace_indent -= 2
            return result

    def str_per_command_line(self):
        if not len(self):
            return '(None)'
        else:
            result = []
            for i, x in enumerate(self, start=1):
                result.append('.%d  %s' % (i, flatstr_per_command_line(x)))
            return '\n'.join(result)


def flatstr(x):
#    if x.__class__.__name__ == 'Scan':  #HACK
#        return str(x)
    if is_listlike(x):
        return ' '.join(flatstr(a) for a in x)
    else:
        return str(x)

def flatstr_per_command_line(x):
    if is_listlike(x):
        return ' '.join(flatstr_per_command_line(a) for a in x)
    else:
        return str_per_command_line(x)


class Pipeline:
    def __init__(self, *stages):
        self.stages = stages

    def __call__(self, x):
        result = x
        for stage in self.stages:
            result = stage(result)
        return result


def run_multiple(f):
    def func(*args):
        if isinstance(args[-1], Multiple):
            return Multiple(*list(
                chain.from_iterable(f(*(args[:-1] + (items,)))
                    for items in args[-1])
            ))
        else:
            return f(*args)
    return func
    
def flatten(lists):
    return list(chain.from_iterable(lists))

def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def lazy(f):
    name = "_" + f.__name__ + "_result"
    @functools.wraps(f)
    def wrapper(self, *args):
        try:
            d = getattr(self, name)
        except AttributeError:
            d = {}
            setattr(self, name, d)
        try:
            return d[args]
        except KeyError:
            d[args] = f(self, *args)
            return d[args]
    return wrapper
    #return functools.lru_cache(maxsize=30)(f)
#    f.cache = {}
#    @functools.wraps(f)
#    def wrapper(*args):
#        try:
#            return f.cache[args]
#        except KeyError:
#            f.cache[args] = result = f(*args)
#            return result
#    return wrapper

def intersperse(separator, iterable):
    return tuple(
        islice(
            chain.from_iterable(zip(repeat(separator), iterable)),
            1,
            None
        )
    )

def updated(d, kv_pairs):
    new_d = d.copy()
    new_d.update(kv_pairs)
    return new_d

def isiterable(x):
    return isinstance(x, collections.Iterable)

def is_listlike(x):
    if type(x) is str:
        return False
    else:
        return isinstance(x, collections.Iterable)

def default(f, deflt=None):
    try:
        return f()
    except:
        return deflt

def first_true(iterable, pred=None, default=None):
    return next(filter(pred, iterable), default)

def safe_unlink(filename):
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass

def safe_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass

re_white_space = re.compile(r'\s+')

def strip_white_space(s):
    return re_white_space.sub('', s)

def number_strs(iterable, f=str):
    for i, x in enumerate(iterable, start=1):
        yield '.%d  %s' % (i, f(x))

def str_per_command_line(o):
    if hasattr(o, 'str_per_command_line'):
        return o.str_per_command_line()
    else:
        return str(o)

def latex(o):
    if hasattr(o, 'latex'):
        return o.latex()
    else:
        return str(o)


class ObjectHolder:

    def __init__(self, initial_object=None):
        self._object = initial_object

    def __getattr__(self, name):
        try:
            return getattr(self._object, name)
        except AttributeError:
            raise

    def __setattr__(self, name, value):
        if name == '_object':
            object.__setattr__(self, '_object', value)
        else:
            return setattr(self._object, name, value)

    def replace_with(self, new_object):
        if isinstance(new_object, ObjectHolder):
            self.replace_with(new_object._object)
        else:
            self._object = new_object

