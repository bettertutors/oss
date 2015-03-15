#!/usr/bin/env python

from json import load
from os import environ, path
from inspect import getmembers, isfunction
from operator import itemgetter
from types import DictType

from utils import pp


def parse_strategy(strategy_file=None):
    # Is it bad not to use proper default variables?
    def inner():
        with open(strategy_file or path.join(path.dirname(__file__), 'strategy.json'), 'r') as f:
            strategy = load(f)

        function_names = map(itemgetter(0), getmembers(inner, isfunction))
        return {k: (lambda f_name: getattr(inner, f_name)(v) if f_name in function_names else v)(to_f_name(k))
                for k, v in strategy.iteritems()}

    to_f_name = lambda f: '{f}_parse'.format(f=f)

    # Do I want to allow `env.` in all fields? - Maybe...
    inner.auth_parse = lambda obj: {k: (environ[v[len('env.'):]] if v.startswith('env.') else v)
                                    for k, v in obj.iteritems()}
    inner.provider_parse = lambda provider: {k: {key: ({'name': lambda: val.upper(),
                                                        'auth': lambda: inner.auth_parse(val)
                                                        }.get(key, val)())
                                                 for key, val in v.iteritems()} if type(v) is DictType else v
                                             for k, v in provider.iteritems()}

    return inner()


def main():
    strategy = parse_strategy()
    pp(strategy)


if __name__ == '__main__':
    main()
