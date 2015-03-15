#!/usr/bin/env python

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

unroll_d = lambda d, *keys: (d[key] for key in keys)
obj_to_d = lambda obj: {k: getattr(obj, k) for k in dir(obj) if not k.startswith('_')}
