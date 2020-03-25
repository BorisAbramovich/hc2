from __future__ import print_function
from __future__ import absolute_import

import logging as _logging
import functools as _functools
import itertools as _itertools
import collections as _collections

_logger = _logging.getLogger(__name__)

flatten = _itertools.chain.from_iterable
"""Concatenates together multiple iterables. See `itertools.chain.from_iterable`."""


def groupby(items, key, multi_value=False):
    """
    Create a dictionary of `key`\(item) => item.

    Examples:
        >>> groupby(range(3), lambda x: x * 2)
        {0: 0, 2: 1, 4: 2}
        >>> groupby(range(6), lambda x: x % 2, multi_value=True)
        {0: [0, 2, 4], 1: [1, 3, 5]}

    Args:
        items (iterable): The items to index.
        key (func): Function to index by.
        multi_value (bool): If True, return a dictionary of `key`\(item) => list of items.

    Returns:
        The index dict.

    Raises:
        ValueError: If `key`\(item) isn't unique and `multi_value` is False.
    """
    idx = {}
    if multi_value:
        for i in items:
            idx.setdefault(key(i), []).append(i)
    else:
        for i in items:
            k = key(i)
            if k in idx:
                raise ValueError("key isn't unique, perhaps use multi_value=True. "
                                 "key={}, values={}".format(k, (idx[k], i)))
            idx[k] = i
    return idx


class IndexableMixin(object):
    """
    Subclasses that implement ``__iter__`` will be lazily indexable; Slicing will behave similar to lists.

    Subclasses must implement ``__iter__`` and optionally ``_slice_collection_type``.

    See `Indexable` for an example implementation.
    """
    __slots__ = ()

    def __getitem__(self, i):
        if isinstance(i, slice):
            start, stop, step = i.start, i.stop, i.step
            # We want to have same functionality as regular list slicing.
            if start is not None:
                start = start.__index__()
            if stop is not None:
                stop = stop.__index__()
            if step is not None:
                step = step.__index__()

            slice_collection_type = getattr(self, '_slice_collection_type', None)
            try:
                items = _itertools.islice(self, start, stop, step)
            except ValueError:
                items = list(self)[start:stop:step]
                if slice_collection_type in (list, None):
                    # If the slice_collection_type is a list, no need to make another copy.
                    # If the slice_collection_type is None, we might as well return a list instead of Indexable.
                    return items
                else:
                    return slice_collection_type(items)
            else:
                if slice_collection_type is None:
                    return Indexable(items)
                else:
                    return slice_collection_type(items)
        else:
            idx = i.__index__()
            if idx < 0:
                return list(self)[idx]
            else:
                return nth(self, idx)


class Indexable(IndexableMixin):
    """
    Allows indexing (similar to lists) on an iterable object.

    Args:
        iterable: The iterable to apply indexing on. If the iterable is infinite then
                  negative slices will cause an infinite loop.
        collection: The type of collection to return when slicing.

    Examples:
        >>> def rng(n): return iter(range(n))
        >>> list(Indexable(rng(5)))
        [0, 1, 2, 3, 4]
        >>> Indexable(rng(5))[3]
        3
        >>> Indexable(rng(5))[-3]
        2
        >>> Indexable(rng(5))[5]
        Traceback (most recent call last):
        IndexError: 5
        >>> Indexable(rng(5), list)[:3:2]
        [0, 2]
        >>> Indexable(rng(5), list)[-2::-2]
        [3, 1]
        >>> list(Indexable(rng(100))[:80][2:][::3][::4]) == list(range(100))[2:80:3*4]
        True
        >>> list(Indexable(rng(100))[::-1])[::-2] == list(range(100))[::2]
        True
        >>> list(Indexable(rng(5), set))
        [0, 1, 2, 3, 4]
        >>> Indexable(rng(5), set)[::2] == set(range(5)[::2])
        True
        >>> Indexable(rng(5), set)[-1:-5:-2] == set(range(5)[-1:-5:-2])
        True
    """

    def __init__(self, iterable, collection=None):
        self._iterable = iterable
        self._slice_collection_type = collection

    def __iter__(self):
        return iter(self._iterable)


class _IndexableGeneratorFactory(IndexableMixin):
    """
    Object returned after decorating a function with `indexify_no_args`.
    Supports ``__iter__`` and ``__getitem__``.

    Args:
        generator_factory (func): A function that takes no arguments and returns a generator.
        collection: The type of collection to return when slicing.
    """

    def __init__(self, generator_factory, collection):
        self._generator_factory = generator_factory
        self._slice_collection_type = collection
        _functools.update_wrapper(self, generator_factory)

    def __iter__(self):
        return self._generator_factory()


def indexify_no_args(collection=None):
    """
    A decorator that takes a function that takes no arguments and returns an iterable,
    and turns it into a list-like `Indexable` object.

    Args:
        collection: The type of collection to return when slicing the `Indexable` object.

    Example:
        >>> @indexify_no_args(list)
        ... def fibss():
        ...     a, b = 0, 1
        ...     while True:
        ...         a, b = b, a + b
        ...         yield b
        >>> fibss[:5]
        [1, 2, 3, 5, 8]
    """

    @_functools.wraps(indexify_no_args)
    def wrapper(f):
        return _IndexableGeneratorFactory(f, collection)

    return wrapper


def indexify(collection=None):
    """
    A decorator that takes a function that returns iterables, and turns it
    into a function that returns list-like `Indexable` objects instead.

    Args:
        collection: The type of collection to return when slicing the function results.

    Example:
        >>> @indexify(list)
        ... def powers(n):
        ...     res = 1
        ...     while True:
        ...         yield res
        ...         res *= n
        >>> powers(3)[:5]
        [1, 3, 9, 27, 81]
    """

    def decorator(generator_factory):
        @_functools.wraps(generator_factory)
        def generator_wrapper(*args, **kwargs):
            return Indexable(generator_factory(*args, **kwargs), collection)

        return generator_wrapper

    return decorator


def first(iterable):
    """
    Return the first item in an iterable.

    >>> first([0, 1])
    0
    >>> first([])
    Traceback (most recent call last):
    ValueError: iterable is empty.
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        raise ValueError('iterable is empty.')


def nth(iterable, n):
    """
    Return the n-th item (0 based).

    >>> nth(range(10), 3)
    3
    >>> nth(range(10), 10)
    Traceback (most recent call last):
    IndexError: 10
    """
    try:
        return next(_itertools.islice(iterable, n, None))
    except StopIteration:
        raise IndexError(n)


def consume(iterator, n=None):
    """
    Advance the iterator `n` steps ahead. If `n` is ``None``, consume entirely.
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        _collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(_itertools.islice(iterator, n, n), None)
    return iterator


def transpose(list_of_lists):
    """
    Transposes a list of lists.

    >>> transpose([[0, 2, 4], [1, 3, 5]])
    [[0, 1], [2, 3], [4, 5]]
    """
    return list(map(list, zip(*list_of_lists)))


def split_true_false(iterable, predicate):
    """
    Return two lists.

    * The items which satisfy the predicate.
    * The items which don't satisfy the predicate.

    >>> split_true_false(range(5), lambda x: x % 2)
    ([1, 3], [0, 2, 4])
    """
    good, bad = [], []
    for i in iterable:
        if predicate(i):
            good.append(i)
        else:
            bad.append(i)
    return good, bad


def split_list(iterable, pred, keep_splits=False):
    """
    Similar to str.split, splits up an iterable on items that satisfy `pred`.

    Args:
        iterable: The items to split into lists.
        pred: The predicate on which to create a new list. `pred` can also be an
              object to compare to.
        keep_splits (bool): If True then items that satisfy the `pred` are added to
                            the beginning of the new list.

    Returns:
        The list of lists.

    >>> split_list([1, 2, 3, 4, 1, 2, 3, 4], lambda x: x > 3)
    [[1, 2, 3], [1, 2, 3], []]
    >>> split_list([1, 2, 3, 4, 1, 2, 3, 4], 4)
    [[1, 2, 3], [1, 2, 3], []]
    >>> split_list([1, 2, 3, 4, 1, 2, 3, 4], 4, True)
    [[1, 2, 3], [4, 1, 2, 3], [4]]
    """
    if not callable(pred):
        split_item = pred

        def pred(x):
            return x == split_item
    lists = []
    curr = []
    for i in iterable:
        if pred(i):
            lists.append(curr)
            curr = [i] if keep_splits else []
        else:
            curr.append(i)
    lists.append(curr)
    return lists


def sublists(lst, sublist_size, jump=1):
    """
    Return sublists of the list.

    >>> list(sublists(list(range(5)), 3))
    [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    >>> list(sublists(list(range(5)), 3, 2))
    [[0, 1, 2], [2, 3, 4]]
    """
    ignored_tail = (len(lst) - sublist_size) % jump
    if ignored_tail:
        _logger.debug('There are %s ignored items.', ignored_tail)
    for i in range(0, len(lst) - sublist_size + 1, jump):
        yield lst[i:i + sublist_size]


def non_unique(items):
    """
    Return the set of non-unique items.

    >>> non_unique([0, 1, 2, 3, 1, 0]) == {0, 1}
    True
    """
    return {i for i, n in _collections.Counter(items).items() if n > 1}


@indexify()
def merge_sorted(iterables):
    """
    Takes a list of sorted iterables, and merges them in a sorted fashion. Note that iterables must be infinite.

    >>> from basics import primes, fibs
    >>> list(merge_sorted([primes, fibs])[:10])
    [1, 2, 2, 3, 3, 5, 5, 7, 8, 11]
    """
    # TODO: can be optimized with heapq
    iterables = [iter(i) for i in iterables]
    nexts = [next(iterable) for iterable in iterables]
    while True:
        next_idx = nexts.index(min(nexts))
        yield nexts[next_idx]
        nexts[next_idx] = next(iterables[next_idx])


def sub_sets(collection, min_size=0, max_size=None):
    """
    Yield all subsets of the given collection.

    Args:
        collection: The collection to return subsets of.
        min_size: The minimum size of the returned sets.
        max_size: The maximum size of the returned sets.

    Example:
        >>> list(sub_sets(range(3), 1, 2))
        [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2)]
    """
    if max_size is None:
        max_size = len(collection)
    return flatten(_itertools.combinations(collection, i) for i in range(min_size, max_size + 1))


def progress_bar_iter(items, label, bar_len=50):
    """
    Wraps an iterable. While iterating over the wrapper, prints a progress bar to stdout.
    """
    items = list(items)
    n = len(items)
    printed_dots = 0
    print('{}: '.format(label), end='')
    for i, item in enumerate(items):
        curr_dots = bar_len * i // n
        curr_dots_to_print = curr_dots - printed_dots
        printed_dots = curr_dots
        print('.' * curr_dots_to_print, end='')
        yield item
    print('.' * (bar_len - printed_dots), 'Done!')
