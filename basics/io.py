from __future__ import absolute_import

import io as _io
import csv as _csv


def read(path, mode='r'):
    """
    Reads the contents of a file into a string.
    """
    with open(path, mode) as f:
        return f.read()


def write(data, path, mode='w'):
    """
    Writes data to a file.
    """
    with open(path, mode) as f:
        f.write(data)


def read_lines(path, remove_empty=True):
    """
    Reads all lines in a file. Optionally ignores empty lines.
    """
    lines = read(path).splitlines()
    if remove_empty:
        lines = list(filter(None, lines))
    return lines


def write_lines(lines, path):
    """
    Writes the lines to a file.
    """
    write('\n'.join(lines), path)


def csv_to_list(csv_string):
    r"""
    Parses a csv string into a list of lists of strings.

    >>> csv_to_list("a,b\r\n1,2\r\n")
    [['a', 'b'], ['1', '2']]
    """
    return list(_csv.reader(_io.StringIO(csv_string)))


def list_to_csv(rows):
    r"""
    Creates a csv string from given rows of values..

    Args:
        rows: An iterable of rows. Each row is an iterable of values.

    >>> list_to_csv([['a', 'b'], ['1', '2']])
    'a,b\r\n1,2\r\n'
    """
    out = _io.StringIO()
    _csv.writer(out).writerows(rows)
    return out.getvalue()


def csv_file_to_list(path):
    """
    Parses a csv file into a list of rows.
    """
    with open(path, newline='') as f:
        return list(_csv.reader(f))


def list_to_csv_file(rows, path):
    """
    Writes given data to a csv file.

    Args:
        rows: An iterable of rows. Each row is an iterable of values.
        path: Path to the csv file to save to.
    """
    with open(path, 'w', newline='') as f:
        _csv.writer(f).writerows(rows)


class InputReader(object):
    """
    A easy to use string input parser.

    Example:
        >>> inp = InputReader('''
        ... good bye
        ... 123
        ... 456
        ... a b
        ... ''')
        >>> inp.lines_left
        4
        >>> inp.words(2)
        ['good', 'bye']
        >>> inp.int()
        123
        >>> inp.digits(3)
        [4, 5, 6]
        >>> inp.chars(3)
        ['a', ' ', 'b']
        >>> inp.lines_left
        0
    """

    def __init__(self, input_string):
        self._lines = input_string.strip().splitlines()
        assert all(self._lines)
        self._next_line = 0

    def line(self):
        return self.lines(1)[0]

    def lines(self, n):
        assert self._next_line + n <= len(self._lines)
        res = self._lines[self._next_line:self._next_line + n]
        self._next_line += n
        return res

    def ints(self, n=None):
        return list(map(int, self.words(n)))

    def chars(self, n=None):
        chars = list(self.line())
        if n is not None:
            assert len(chars) == n
        return chars

    def words(self, n=None):
        words = self.line().split()
        if n is not None:
            assert len(words) == n
        return words

    def digits(self, n=None):
        return list(map(int, self.chars(n)))

    def floats(self, n=None):
        return list(map(float, self.words(n)))

    def int(self):
        return int(self.word())

    def char(self):
        return self.chars(1)[0]

    def word(self):
        return self.words(1)[0]

    def digit(self):
        return int(self.char())

    def float(self):
        return float(self.word())

    @property
    def lines_left(self):
        return len(self._lines) - self._next_line
