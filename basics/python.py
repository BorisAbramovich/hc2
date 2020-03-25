from __future__ import print_function

import re as _re
import sys as _sys
import enum as _enum
import inspect as _inspect
import logging as _logging
import functools as _functools
#import six as _six

try:
    import copyreg as _copyreg
except ImportError:
    import copy_reg as _copyreg

_logger = _logging.getLogger(__name__)

try:
    memoize = _functools.lru_cache(maxsize=None)
    """A decorator that caches results of a function. See `functools.lru_cache`."""
except AttributeError:
    def memoize(f):
        cache = {}

        def wrapper(*args, **kwargs):
            key = args, frozenset(kwargs.items())
            if key not in cache:
                cache[key] = f(*args, **kwargs)
            return cache[key]

        return wrapper


def log_calls(f):
    """
    A decorator that logs calls to a function to the standard output.
    """

    @_functools.wraps(f)
    def _log_calls(*args, **kwargs):
        str_args = list(map(repr, args))
        str_kwargs = ['{}={}'.format(k, repr(v)) for k, v in kwargs.items()]
        all_args = ', '.join(str_args + str_kwargs)
        call_str = '{}({})'.format(f.__name__, all_args)
        print(call_str)
        ans = f(*args, **kwargs)
        # print('{}({}) = {}'.format(f.__name__, all_args, repr(ans)))
        return ans

    return _log_calls


def log_call_detailed():
    """
    A function that logs calls to a function. Call log_call_detailed inside the function you want to log.

    Example:
        >>> def division(a, b):
        ...     if b == 0:
        ...         log_call_detailed()
        ...     return a / b
    """
    frame = _sys._getframe(1)
    arg_str = _inspect.formatargvalues(*_inspect.getargvalues(frame))
    _logger.debug(frame.f_code.co_name + arg_str)


class dictify(object):
    """
    Decorator that turns a function into an indexable object.

    Useful when APIs only accept ``dict``-like arguments.
    Note that keyword arguments aren't supported.

    >>> @dictify
    ... def neg(n):
    ...     return -n
    >>> neg[123]
    -123
    """

    def __init__(self, f):
        _functools.update_wrapper(self, f)
        self._f = f

    def __getitem__(self, args):
        if isinstance(args, tuple):
            return self._f(*args)
        else:
            return self._f(args)


_FORMATT_RE = _re.compile(r"\{((?:[^}]*\])*[^:}]*)([^}]*)\}")


@memoize
def _parse_formatt_template(template):
    """
    Parses a formatt template and returns the format template and compiled format argument code snippets.
    """
    matches = _FORMATT_RE.finditer(template)
    format_args = tuple(compile(m.group(1), '', 'eval') for m in matches)
    format_template = _FORMATT_RE.sub(r'{\2}', template)
    return format_template, format_args


def formatt(template):
    """
    Similar to `str.format` but code snippets can be written inside the ``{}`` before the formating options.

    Examples:
        >>> formatt('1 + 2 is {1 + 2}')
        '1 + 2 is 3'
        >>> formatt('Pi to the second digit is {3.1415926:.2f}')
        'Pi to the second digit is 3.14'
        >>> formatt('Pi to the second digit is {3.1415926:.2f}')
        'Pi to the second digit is 3.14'
        >>> name = 'joseph'
        >>> formatt('My name: {name.capitalize():.<9}')
        'My name: Joseph...'
        >>> formatt('Some numbers: {str(range(10)[:3]):.<13}')
        'Some numbers: range(0, 3)..'
    """
    frame = _sys._getframe(1)
    frame_globals = frame.f_globals
    frame_locals = frame.f_locals

    format_template, format_arg_codes = _parse_formatt_template(template)
    format_args = []
    for code_to_eval in format_arg_codes:
        result = eval(code_to_eval, frame_globals, frame_locals)
        format_args.append(result)
    return format_template.format(*format_args)


def printt(formatt_template, **print_kwargs):
    """
    Similar to print. Uses a template instead of a list of arguments.

    See `formatt` for more information.
    """
    _sys._getframe(0).f_locals.update(_sys._getframe(1).f_locals)
    print(formatt(formatt_template), **print_kwargs)


def find_attrs(obj, *substrings, **kwargs):
    """
    Prints attributes of an object or objects that contain certain sub-strings.

    Args:
        obj: An object or `tuple` of objects for which to search for attributes.
        substrings: The sub-strings to search for (case-insensitive) in the object attributes.
        must_contain_all: If True then only attributes that contain all sub-strings will be printed.
    """
    must_contain_all = kwargs.pop('must_contain_all', False)
    if isinstance(obj, tuple):
        objs = obj
    else:
        objs = (obj,)
    substrings = tuple(s.lower() for s in substrings)
    pred = all if must_contain_all else any
    for obj in objs:
        dir_obj = (attr.lower() for attr in dir(obj))
        attrs = [attr for attr in dir_obj if pred(sub in attr for sub in substrings)]
        if not attrs:
            attrs = ['None']
        print('Attributes of {}:\n    {}\n\n'.format(repr(obj), '\n    '.join(attrs)))


def remove_modules(prefix):
    """
    Removes modules whose names start with `prefix` from `sys.modules`.
    """
    modules_to_remove = [m for m in _sys.modules if m.startswith(prefix)]
    for m in modules_to_remove:
        del _sys.modules[m]


class _DefaultEnumMeta(_enum.EnumMeta):
    def __call__(cls, value):
        try:
            return super().__call__(value)
        except ValueError:
            _logging.getLogger(cls.__module__ + '.' + cls.__name__).debug('Unknown value: %s.', repr(value))
            return cls._default


# class DefaultEnum(_six.with_metaclass(_DefaultEnumMeta, _enum.Enum)):
#     """
#     Enum class that supports giving a default enum value.
#
#     Example:
#         >>> class MyEnum(DefaultEnum):
#         ...     a = 1
#         ...     b = 2
#         ...     unknown = 3
#         ...     _default = unknown  # Here we set unknown as the default value.
#         >>> MyEnum(123)
#         <MyEnum.unknown: 3>
#     """
#     pass


class lazy_property(object):
    """
    Similar to `property` but the result is calculated once and cached in the object's ``__dict__``.
    """

    def __init__(self, method):
        _functools.update_wrapper(self, method)
        self._method = method

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            result = self._method(instance)
            setattr(self, self._method.__name__, result)
            return result


def slots(obj):
    """
    Returns all slot attributes of the object in a dictionary.
    """
    d = {}
    for k in _copyreg._slotnames(type(obj)):
        try:
            d[k] = object.__getattribute__(obj, k)
        except AttributeError:
            pass
    return d


def safe_getattrs(obj):
    """
    Returns all slot/``__dict__`` attributes of the object in a dictionary.
    """
    d = slots(obj)
    try:
        d.update(object.__getattribute__(obj, '__dict__'))
    except AttributeError:
        pass
    return d
