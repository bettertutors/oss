#!/usr/bin/env python

from types import DictType, NoneType
from itertools import ifilter
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

unroll_d = lambda d, *keys: (d[key] for key in keys)
obj_to_d = lambda obj: {k: getattr(obj, k) for k in dir(obj) if not k.startswith('_')}

find_one = lambda key, enumerable, attr: next(ifilter(lambda obj: getattr(obj, attr) == key, enumerable))
find_one.__doc__ == """ @raises `StopIteration` if not found """


def raise_f(exception, *args, **kwargs):
    raise exception(*args, **kwargs)


def find_by_key(d, key):
    """
        :param d :type DictType
        :param key :type instanceof basestring
    """
    if key in d:
        return d[key]

    for k, v in d.iteritems():
        if type(v) is DictType:
            item = find_by_key(v, key)
            if type(item) is not NoneType:
                return item
    raise ValueError('"{key}" not found'.format(key=key))
