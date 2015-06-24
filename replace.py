from itertools import product, chain, zip_longest, islice
from abc import ABCMeta, abstractmethod
from collections import namedtuple

from misc import updated, dd, trace, default, Multiple, is_listlike, flatten, \
    run_multiple, lazy
from testing import reduce_to_text
from source import force_source_from


class CombinatoricMap:

    def __init__(self, rw_fixup, *pairs):
        self.rw_fixup = rw_fixup
        self.pairs = pairs

    def __call__(self, x):
        return self.map(x)

    @run_multiple
    def map(self, x):
        result = []
        xtail = x
        while len(xtail) >= 1:
            matching_pair, xtail, env = self.find_matching_pair(xtail, {})
            if matching_pair is None:
                return Multiple()
            else:
                matched, replace_with = matching_pair
                replacement = replace_with.replace(self.rw_fixup, matched, env)
                if len(replacement):
                    result.append(replacement)
        return Multiple(*(
            tuple(chain.from_iterable(elem))
                for elem in product(*result)
        ))

    def find_matching_pair(self, x, env):
        for pair in self.pairs:
            target, replace_with = pair
            matched, xtail, new_env = target.match(x, env)
            if xtail is None:
                continue
            else:
                return (matched, replace_with), xtail, new_env
        return None, None, None


class Filter:

    def __init__(self, *disallows):
        self.disallows = disallows

    def __call__(self, multiple):
        return Multiple(*[
            item
                for item in multiple
                    if self.is_ok(item)
        ])

    def is_ok(self, item):
        return all(disallow.is_ok(item) for disallow in self.disallows)


class Target:

    def __init__(self, *target_seq):
        self.seq = target_seq

    #TODO Get rid of this. It's superseded by self.matches.
    def match(self, x, env):
        seq = self.seq
        xtail = x
        total_matched = []
        while len(seq) >= 1:
            matched, xtail, env = match_one(xtail, seq[0], env)
            if matched is None:
                return None, None, None
            seq = seq[1:]
            total_matched = total_matched + matched
        return total_matched, xtail, env

    def is_match(self, x, env):
        matched, xtail, new_env = self.match(x, env)
        return matched is not None

    def matches(self, x, env):
        matched_items, xtail, env = self.match(x, env)
        if matched_items is None:
            return []
        else:
            return [Match(self, matched_items, xtail, env)]

    def match_and_replace(self, x, env):
        matches = self.matches(x, env)
        return [
            make_replacements(match, [self.seq])
                for match in matches
        ]

    def subst(self, env):
        return [flatten(
            make_substitution(elem, env)
                for elem in self.seq
        )]

    def __repr__(self):
        return 'Target(%s)' % ', '.join(repr(x) for x in self.seq)


def match_one(x, target_elem, env):
    if isinstance(target_elem, Target):
        return target_elem.match(x, env)
    elif len(x) == 0:
        return None, None, None
    elif isinstance(x[0], CanMatchTargetElem):
        if x[0].matches_target_elem(target_elem):
            return [x[0]], x[1:], env
        else:
            return None, None, None
    else:
        if x[0] == target_elem:
            return [x[0]], x[1:], env
        else:
            return None, None, None


class Disallow(Target):

    def __init__(self, *disallowed_subsequence):
        self.seq = disallowed_subsequence

    def is_ok(self, x):
        env = {}
        return not any(
            self.is_match(x[index:], env)
                for index in range(len(x))
        )


class CanMatchTargetElem(metaclass=ABCMeta):

    @abstractmethod
    def matches_target_elem(self, target_elem):
        pass


class ReplaceWith:

    def __init__(self, *replacements):
        self.replacements = replacements

    def replace(self, rw_fixup, matched, env):
        return [
            self._replace_one(replacement, rw_fixup, matched, env)
                for replacement in self.replacements
        ]

    def _replace_one(self, replacement, rw_fixup, matched, env):
        elems_and_matches = islice(
            zip_longest(
                self._substitutions(replacement, env),
                matched,
                fillvalue=default(lambda: matched[-1])
            ),
            len(replacement)
        )
        return [
            rw_fixup(
                elem,
                force_source_from(one_matched)
            )
                for (elem, one_matched) in elems_and_matches
        ]

    def _substitution(self, elem, env):
        if hasattr(elem, 'subst'):
            return elem.subst(env)
        else:
            return [elem]

    def _substitutions(self, replacement, env):
        return flatten([
            self._substitution(elem, env)
                for elem in replacement
        ])

    def __repr__(self):
        return 'ReplaceWith(%s)' % ', '.join(repr(x) for x in self.replacements)


class MakeInto:

    def __init__(self, make_into_class):
        self.make_into_class = make_into_class

    def __call__(self, rw_object, source):
        if isinstance(rw_object, self.make_into_class):
            return rw_object
        else:
            return self.make_into_class(rw_object, source=source)

    def __repr__(self):
        return 'MakeInto(%s)' % repr(self.make_into_class)

#TODO Rename this to something better.
def ignore_matched_input(rw_object, source):
    return rw_object


class Make:

    def __init__(self, ctor, *args):
        self.ctor = ctor
        self.args = args

    def subst(self, env):
        return [self.ctor(*fill_in_variables(self.args, env))]

    def __repr__(self):
        items = [repr(self.ctor)] + [repr(arg) for arg in self.args]
        return 'Make(%s)' % ', '.join(items)

def fill_in_variables(args, env):
    return flatten([
        env.get(arg.name) if isinstance(arg, Var) else [arg]
            for arg in args
    ])


class Class_Any(Target):

    def match(self, x, env):
        if len(x) >= 1:
            return [x[0]], x[1:], env
        else:
            return None, None, None

    def __repr__(self):
        return 'Any'

Any = Class_Any()


class Var(Target):

    def __init__(self, name, target=Any):
        self.name = name
        self.target = target

    def match(self, x, env):
        matched, xtail, new_env = self.target.match(x, env)
        if matched is not None:
            new_env = updated(new_env, [(self.name, matched)])
        return matched, xtail, new_env

    def subst(self, env):
        return env.get(self.name)

    def __repr__(self):
        return 'Var(%s, %s)' % (repr(self.name), repr(self.target))


class TestVar(Var):

    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def match(self, x, env):
        if len(x) >= 1 and self.condition(x[0]):
            return [x[0]], x[1:], updated(env, ((self.name, [x[0]]),))
        else:
            return None, None, None

    def __repr__(self):
        return 'TestVar(%s)' % repr(self.name)


class Optional(Target):

    def __init__(self, *optional_seq):
        self.target = Target(*optional_seq)

    def match(self, x, env):
        matched, xtail, new_env = self.target.match(x, env)
        if matched is None:
            return [], x, env
        else:
            return matched, xtail, new_env

    def __repr__(self):
        return 'Optional(%s)' % str(self.target)


class NotFollowedBy(Target):

    def __init__(self, *seq):
        self.target = Target(*seq)

    def match(self, x, env):
        matched, xtail, new_env = self.target.match(x, env)
        if matched is None:
            return [], x, env
        else:
            return None, None, None
        
    def __repr__(self):
        return 'NotFollowedBy(%s)' % str(self.target)


class CombinatoricSequence:

    def __init__(self, alternativess=[]):
        self.alternativess = alternativess

    def append(self, alternatives):
        return CombinatoricSequence(self.alternativess + [alternatives])

    @property
    @lazy
    def product(self):
        return Multiple(*product(*self.alternativess))

    def __repr__(self):
        return 'CombinatoricSequence(%s)' % ', '.join(
            repr(a) for a in self.alternativess
        )


class CombinatoricAlternatives:

    def __init__(self, *alternatives):
        self.alternatives = alternatives

    def __iter__(self):
        return iter(self.alternatives)

    def make_substitutions(self, env):
        return CombinatoricAlternatives(*flatten(
            flatten(make_substitution(alt, env)) for alt in self.alternatives
        ))

    def __repr__(self):
        return '\nCombinatoricAlternatives(%s)' % ', '.join(
            repr(reduce_to_text(a)) for a in self.alternatives
        )


class ResultContinuation:

    @classmethod
    def start(cls, x, chunks):
        return ResultContinuation(CombinatoricSequence(), x, chunks, {})

    def __init__(self, results, xtail, chunks_tail, env):
        self.results = results  # CombinatoricSequence
        self.xtail = xtail
        self.chunks_tail = chunks_tail
        self.env = env

    @property
    def is_pending(self):
        return len(self.xtail) > 0 and len(self.chunks_tail) > 0

    @property
    def is_done(self):
        return len(self.xtail) == 0 and len(self.chunks_tail) == 0

    def new_ks(self):
        chunk_results = self.chunks_tail[0].match_and_replace(
            self.xtail, self.env
        )
        tentative_results = [
            ResultContinuation(
                self.results.append(chunk_result.replacements),
                chunk_result.xtail,
                self.chunks_tail[1:],
                chunk_result.env
            )
                for chunk_result in chunk_results
        ]
        return [
            new_k
                for new_k in tentative_results
                    if new_k.is_done or new_k.is_pending
        ]

    def make_multiple(self):
        return self.results.product


Match = namedtuple('Match', ['matched_target', 'matched_items', 'xtail', 'env'])
ChunkResult = namedtuple('ChunkResult', ['replacements', 'xtail', 'env'])


class ParseInto:

    def __init__(self, *chunks):
        self.chunks = chunks

    @run_multiple
    def __call__(self, x):
        result_continuations = [ResultContinuation.start(x, self.chunks)]
        pending_ks, done_ks = self.partition_ks(result_continuations)
        while pending_ks:
            new_ks = flatten(
                k.new_ks() for k in pending_ks
            )
            result_continuations = done_ks + new_ks
            pending_ks, done_ks = self.partition_ks(result_continuations)
        return Multiple(*
            flatten(k.make_multiple() for k in result_continuations)
        )

    @classmethod
    def partition_ks(cls, result_continuations):
        return (
            [k for k in result_continuations if k.is_pending],
            [k for k in result_continuations if k.is_done]
        )


class Chunk:

    def __init__(self, old, new):
        self.old = old if isinstance(old, Target) else Target(*old)
        self.new = CombinatoricAlternatives(*new)

    def match_and_replace(self, x, env):
        """Returns a list of ChunkResults."""
        matches = self.old.matches(x, env)
        return [
            make_replacements(match, self.new)
                for match in matches
        ]

    def __repr__(self):
        return 'Chunk(old=%s, new=%s)' % (repr(self.old), repr(self.new))


def make_substitution(elem, env):
    # Encloses its answer in a list, no matter what. This enables a .subst()
    # method to transform a single item into multiple items.
    if hasattr(elem, 'subst'):
        return elem.subst(env)
    elif is_listlike(elem):
        return [flatten(make_substitution(e, env) for e in elem)]
    else:
        return [elem]

def make_replacements(match, alternatives):
    env = (
        match.env
        if 'OLD' in match.env
        else updated(match.env, [('OLD', match.matched_items)])
    )
    return ChunkResult(
        alternatives.make_substitutions(env),
        match.xtail,
        match.env
    )


def is_target(x):
    return hasattr(x, 'matches')

def make_chunk(x):
    if hasattr(x, 'match_and_replace'):  # ideally:  if isinstance(x, Chunk):
        return x
    elif is_listlike(x):
        return Chunk(old=x, new=[[x]])
    else:
        return Chunk(old=[x], new=[[x]])


#TODO rm Target?
class Or(Target, Chunk):

    def __init__(self, *chunks):
        self.chunks = [make_chunk(ch) for ch in chunks]

    def match_and_replace(self, x, env):
        return flatten([
            chunk.match_and_replace(x, env)
                for chunk in self.chunks
        ])

    #TODO rm?
    def matches(self, x, env):
        return flatten(
            chunk.matches(x, env)
                for chunk in self.chunks
        )

    def __repr__(self):
        return 'Or(%s)' % ', '.join(repr(t) for t in self.chunks)
