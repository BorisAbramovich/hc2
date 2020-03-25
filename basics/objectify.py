import json as _json


class ObjectList(list):
    """
    A list whose first item can be accessed by the attribute ``f`` allowing tab-completion. See `objectify`.

    The ``repr`` is also changed.
    """

    def __init__(self, lst):
        super().__init__(map(objectify, lst))
        if self:
            self.f = self[0]

    def __repr__(self):
        return '. ' + '\n. '.join(str(i).replace('\n', '\n  ') for i in self)

    def _unobjectify(self):
        return unobjectify(self)


class ObjectDict(object):
    """
    An object that wraps a dictionary allowing tab-completion. See `objectify`.

    >>> o = ObjectDict({'a': {'aa': 1}, 'b': 2})
    >>> o.a.aa
    1
    """

    def __init__(self, dct):
        if isinstance(dct, str):
            dct = _json.loads(dct)
        self.__dict__.update((k, objectify(v)) for k, v in dct.items())

    def __repr__(self):
        parts = []
        for k, v in self.__dict__.items():
            if isinstance(v, ObjectDict):
                parts.append('{}:\n  {}'.format(k, str(v).replace('\n', '\n  ')))
            elif isinstance(v, ObjectList):
                parts.append('{}:\n{}'.format(k, v))
            else:
                parts.append('{}: {}'.format(k, str(v).replace('\n', '\n' + ' ' * (len(str(k)) + 2))))
        parts = sorted(parts, key=lambda i: (i.count('\n'), i))
        return '\n'.join(parts)

    def _unobjectify(self):
        return unobjectify(self)


def objectify(obj):
    """
    Converts a json-like dict or list into a user-friendly object with a succinct ``repr`` and tab completion.
    """
    if isinstance(obj, dict):
        return ObjectDict(obj)
    elif isinstance(obj, list):
        return ObjectList(obj)
    else:
        return obj


def unobjectify(obj):
    """
    Converts an objectified object back into a json-like dict or list.
    """
    if isinstance(obj, ObjectDict):
        return {k: unobjectify(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, ObjectList):
        return [unobjectify(x) for x in obj]
    else:
        return obj
