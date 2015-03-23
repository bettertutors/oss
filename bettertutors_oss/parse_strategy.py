#!/usr/bin/env python

from json import loads
from os import path
from inspect import getmembers, isfunction
from operator import itemgetter

from bettertutors_oss.utils import pp
from bettertutors_oss.parser.env import parse_out_env
from bettertutors_oss.Strategy import Strategy


def parse_strategy(strategy_file=None):
    # Is it bad not to use proper default variables?

    def inner():
        with open(strategy_file
                  or path.join(path.realpath(path.dirname(__file__)), 'config', 'strategy.sample.json'), 'r') as f:
            s = parse_out_env(f.read())
        strategy = loads(s)

        function_names = map(itemgetter(0), getmembers(inner, isfunction))
        return {k: (lambda f_name: getattr(inner, f_name)(v) if f_name in function_names else v)(to_f_name(k))
                for k, v in strategy.iteritems()}

    to_f_name = lambda f: '{f}_parse'.format(f=f)

    inner.provider_parse = lambda provider: {
        k: map(lambda option: {key.upper(): val for key, val in option.iteritems()}, v)
        for k, v in provider.iteritems()
    }

    return inner()


def main():
    strategy = parse_strategy()
    strategy = Strategy(strategy)
    pp(strategy)


if __name__ == '__main__':
    main()
