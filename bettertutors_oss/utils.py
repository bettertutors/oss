#!/usr/bin/env python

# FYI: Bad practice to put a utils like this, will push it somewhere else [eventually!]

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


from collections import Counter


def subsequence(many_d):
    """
        :param many_d enumerable containing many :type DictType
        :returns entries which are common between all :type TupleType

        Example:
             >>> ds = {'a': 5, 'b': 6}, {'a': 5}, {'a': 7}
             >>> subsequence(ds)
             >>> ('a;;;5',)
    """
    c = Counter()
    for d in many_d:
        for k, v in d.iteritems():
            c['{0};;;{1}'.format(k, v)] += 0.5
    for k, v in c.iteritems():
        c[k] = int(v)  # Remove all halves, and enable `.elements` to work
    return tuple(c.elements())


find_common_d = lambda target_d, ds: next(d for d in ds
                                          if any(getattr(d, k) == v for k, v in target_d.iteritems()
                                                 if k in obj_to_d(d)))
