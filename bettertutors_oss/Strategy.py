from json import loads
from os import path
from inspect import getmembers, isfunction
from operator import itemgetter
from random import randint

from bettertutors_oss.parser.env import parse_out_env


class Strategy(object):
    def __init__(self, strategy_filename):  # Default gets propagated down
        self.strategy = self._parse(strategy_filename)
        self.default_pick = self.strategy['default_pick']

    def get_os(self, offset=0):
        return self._get_next_option(self.strategy['node']['os'], offset)

    def get_hardware(self, offset=0):
        return self._get_next_option(self.strategy['node']['hardware'], offset)

    def get_location(self, offset=0):
        return self._get_next_option(self.strategy['node']['location'], offset)

    def get_provider(self, offset=0):
        return self._get_next_option(self.strategy['provider'], offset)

    @staticmethod
    def _parse(strategy_filename):
        def inner():
            with open(strategy_filename, 'r') as f:
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

    def _get_next_option(self, obj, offset=0):
        obj = obj.copy()
        pick = obj.get('pick', self.default_pick)
        return obj['options'][offset:][self._pick(pick, len(obj['options']), offset)]

    _pick = lambda self, algorithm, length, offset: {
        'first': 0,
        'random': randint(offset, length)
    }[algorithm]


if __name__ == '__main__':
    pass
