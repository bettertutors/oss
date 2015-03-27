from json import loads
from inspect import getmembers, isfunction
from operator import itemgetter
from random import randint

from bettertutors_oss.parser.env import parse_out_env
from bettertutors_oss.utils import raise_f, find_one, find_by_key, find_common_d, obj_to_d


class Strategy(object):
    def __init__(self, strategy_filename):  # Default gets propagated down
        self.strategy = self._parse(strategy_filename)
        self.default_pick = self.strategy['default_pick']

    def get_image(self, offset=0):
        return self._get_next_option(self.strategy['node']['image'], offset)

    def get_hardware(self, offset=0):
        return self._get_next_option(self.strategy['node']['hardware'], offset)

    def get_location(self, offset=0):
        return self._get_next_option(self.strategy['node']['location'], offset)

    def get_provider(self, offset=0):
        return self._get_next_option(self.strategy['provider'], offset)

    def get_option(self, name, enumerable):
        for i in xrange(len(find_by_key(self.strategy, name)['options'])):
            try:
                return find_common_d(
                    ds=enumerable, target_d=getattr(self, 'get_{name}'.format(name=name))(offset=i)
                )
            except StopIteration:
                pass
        raise ValueError('Failed to set "{name}"'.format(name=name))

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

    _get_next_option = lambda self, obj, offset=0: obj['options'][offset:][
        self._pick(obj.get('pick', self.default_pick), len(obj['options']))
    ]

    _pick = lambda self, algorithm, length: {
        'first': 0,
        'random': randint(0, length)
    }[algorithm] if length else raise_f(ValueError, '`_pick` performed on empty list')


if __name__ == '__main__':
    pass
