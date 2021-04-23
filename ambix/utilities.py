import collections
import itertools


def iter_not_string(val):
    """
    Returns true if the argument is iterable but not a string
    """
    return isinstance(val, collections.Iterable) and not isinstance(val, str)


def compose_iters(*args):
    """
    flattens iterables passed as arguments into a single iterable collection
    """
    return itertools.chain(*(i if iter_not_string(i) else [i] for i in args))


def pairwise(seq):
    return zip(seq, seq[1:])
