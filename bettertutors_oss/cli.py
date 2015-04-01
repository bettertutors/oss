from os import path
from functools import partial
from argparse import ArgumentParser

from jsonschema import validate as jsonschema_validation

from bettertutors_oss.utils import obj_to_d, pp

config_join = partial(path.join, path.realpath(path.dirname(__file__)), 'config')


def _build_parser():
    parser = ArgumentParser(description='Deploy/create/manage compute nodes')
    parser.add_argument('-s', '--strategy', help='strategy file [strategy.sample.json]',
                        default=config_join('strategy.sample.json'))
    parser.add_argument('-n', '--no-validation', help='Skip JSON-Schema validation',
                        default=False, action='store_true')
    parser.add_argument('-c', '--compute', help='Run compute with strategy [True]',
                        default=True, action='store_true')
    return parser


if __name__ == '__main__':
    args = _build_parser().parse_args()
    print "config_join('schema.json') =", config_join('schema.json')
    if not args.no_validation:
        import json

        jsonschema_validation(instance=args.strategy,
                              schema=json.load(open(config_join('schema.json'))))
    if args.compute:
        print args
    pp(obj_to_d(args))
