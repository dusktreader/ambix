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
