#!/usr/bin/env python

from json import load
from os import environ
from sys import modules
from inspect import getmembers, isfunction
from operator import itemgetter

from utils import pp


def parse_strategy(strategy_file='strategy.json'):
    if not strategy_file:  # Bad hack? - Should it just throw an exception?
        strategy_file = 'strategy.json'

    with open(strategy_file, 'r') as f:
        strategy = load(f)

    function_names = map(itemgetter(0), getmembers(modules[__name__], isfunction))

    return {k: (globals()[_to_f_name(k)](v) if _to_f_name(k) in function_names else v)
            for k, v in strategy.iteritems()}


_to_f_name = lambda v: '_{v}_parse'.format(v=v)
# Do I want to allow `env.` in all fields? - Maybe...
_auth_parse = lambda auth: {k: (environ[v[len('env.'):]] if v.startswith('env.') else v)
                            for k, v in auth.iteritems()}
_provider_parse = lambda provider: provider.upper()


def main():
    strategy = parse_strategy()
    pp(strategy)


if __name__ == '__main__':
    main()
