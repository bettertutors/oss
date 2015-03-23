from json import loads
from os import path
from inspect import getmembers, isfunction
from operator import itemgetter

from bettertutors_oss.parser.env import parse_out_env


class Strategy(object):
    def __init__(self, strategy_filename):  # Default gets propagated down
        self.strategy = self._parse(strategy_filename)
        self.default_pick = self.strategy['default_pick']

    def get_os(self):
        return self._get_next_option(self.strategy['node']['os'])

    def get_hardware(self):
        return self._get_next_option(self.strategy['node']['hardware'])

    def get_location(self):
        return self._get_next_option(self.strategy['node']['location'])

    def get_provider(self):
        return self._get_next_option(self.strategy['provider'])

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

    def _get_next_option(self, obj, last=0):
        obj = obj.copy()
        pick = obj.get('pick', self.default_pick)
        return obj['options'][last:][self._pick(pick, len(obj['options']))]

    _pick = lambda self, algorithm, length, offset=0: {
        'first': 0
    }[algorithm]


if __name__ == '__main__':
    pass
