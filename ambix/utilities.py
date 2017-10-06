import collections
import itertools
import re
import textwrap


def dedent(text):
    """
    Dedents a block of indented text and removes any leading or tailing
    whitespace for the block
    """
    return textwrap.dedent(text).strip()


def strip_whitespace(text):
    """
    Removes all whitespace from a string
    """
    return re.sub(r'\s+', '', text)


def iter_not_string(val):
    """
    Returns true if the argument is iterable but not a string
    """
    return (isinstance(val, collections.Iterable) and not isinstance(val, str))


def compose_iters(*args):
    """
    flattens iterables passed as arguments into a single iterable collection
    """
    return itertools.chain(*(i if iter_not_string(i) else [i] for i in args))


def pairwise(seq):
    return zip(seq, seq[1:])
