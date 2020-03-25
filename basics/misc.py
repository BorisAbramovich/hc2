import re as _re
import time as _time
import string as _string
import logging as _logging
import operator as _operator

from basics.io_name import read, InputReader, write_lines

_logger = _logging.getLogger(__name__)


def bits(bytes_):
    r"""
    Return the bit format of bytes.

    Args:
        bytes_ (bytes, str): The bytes to convert to bit format. If given a `str`, it will be encoded using 'ascii'

    >>> bits(b'\x80\x0F')
    '1000000000001111'
    >>> bits('aA')
    '0110000101000001'
    """
    if isinstance(bytes_, str):
        bytes_ = bytes_.encode('ascii')
    return ''.join('{:08b}'.format(c) for c in bytes_)


def is_palindrome(s):
    """
    Return whether s is a palindrome.

    >>> is_palindrome('12321')
    True
    >>> is_palindrome('123')
    False
    """
    return s == s[::-1]


def jagged_to_square(list_of_lists, fill_item):
    """
    Turns a jagged list of lists into a square list of lists inplace.

    Args:
        list_of_lists: A list of lists of varying lengths.
        fill_item: The item to append to short lists.

    Example:
        >>> lsts = [[1, 2, 3], [4, 5]]
        >>> jagged_to_square(lsts, 0)
        >>> lsts
        [[1, 2, 3], [4, 5, 0]]
    """
    max_len = max(len(lst) for lst in list_of_lists)
    for lst in list_of_lists:
        lst.extend([fill_item] * (max_len - len(lst)))


_printables = set(_string.printable)


def is_printable(s):
    """
    Return whether the string is printable.
    """
    return set(s).issubset(_printables)


def google_code(func, input_file, output_file):
    inp = InputReader(read(input_file))
    t = inp.int()
    outputs = []
    for t in range(t):
        try:
            outputs.append(func(inp))
        except:
            for _ in range(5):
                print("Error for Case #{}".format(t))
            raise

    outputs = ["Case #{}: {}".format(i, str(out)) for i, out in enumerate(outputs, 1)]
    write_lines(output_file, outputs)
    print("DONE!")


def xor_bytes(bytes1, bytes2):
    r"""
    >>> xor_bytes(b'\x0a\x01', b'\xa0\xFF')
    b'\xaa\xfe'
    """
    return bytes(map(_operator.xor, bytes1, bytes2))


class Stopwatch(object):
    """
    A stopwatch can be used to time code.

    Example ::

        sw = Stopwatch()
        # Do some work...
        elapsed = sw.elapsed_seconds

    The stopwatch can also be used as a context manager. On completion, the elapsed time is logged. ::

        with Stopwatch('foo'):
            # Do some work...
    """

    def __init__(self, identifier=''):
        self.identifier = identifier
        self.start_time = _time.clock()

    @property
    def elapsed_seconds(self):
        return _time.clock() - self.start_time

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        _logger.debug('%s exited in %s seconds.', self, self.elapsed_seconds)

    def __repr__(self):
        return 'Stopwatch({})'.format(self.identifier)


def re_strip(string, regexs):
    r"""

    :param string:
    :param regexs:
    :return:

     Example:
         >>> re_strip('asdasd Hello asdddd', ('\s', '[asd]'))
         'Hello'
         >>> re_strip('\t  \n  <br/>   World \n  \t  <br/>  ', ('\s', '<br/>'))
         'World'
    """
    if isinstance(regexs, str):
        regexs = (regexs,)
    wrapped_regexes = ['(?:{})'.format(r) for r in regexs]
    all_regexs = '(?:{})'.format('|'.join(wrapped_regexes))
    stripping_regex = '{0}*(.*?){0}*$'.format(all_regexs)
    match = _re.match(stripping_regex, string)
    return match.group(1)
