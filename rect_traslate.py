"""
Translate numbers into characters.  Return data as a string
"""


def translate(rectangle):
    """
    Convert rectangle numbers to pentomino characters
    """
    return '\n'.join(tuple(map(_line_conv, rectangle))) + '\n\n'


def _line_conv(chars_to_conv):
    """
    Convert a row of the rectangle from numbers to pentomino characters
    """
    return ''.join(tuple(map(_fconvert, chars_to_conv)))


def _fconvert(value):
    """
    Convert one tile from a number to a pentomino character
    """
    return {523: 'U', 39: 'N', 15: 'F', 135: 'W', 23: 'P', 267: 'L',
            139: 'Z', 77: 'T', 85: 'Y', 43: 'V', 33033: 'I', 29: 'X'}[value]
