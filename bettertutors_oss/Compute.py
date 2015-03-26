#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from collections import Callable
from itertools import ifilter

from libcloud.compute.types import Provider, LibcloudError
from libcloud.compute.providers import get_driver

from Strategy import Strategy
from utils import pp, obj_to_d, find_one


class Compute(object):
    """ Light wrapper around libcloud to facilitate integration with strategy files,
        and simplification of commands """

    offset = 0
    node = None

    def set_node(self):
        provider_name, provider = (
            lambda _provider_obj: (lambda name: (name, _provider_obj[name]))(_provider_obj.keys()[0])
        )(self.strategy.get_provider(self.offset))

        # TODO: Inherit from `conn`
        (lambda class_: tuple(setattr(self, attr, getattr(class_, attr))
                              for attr in filter(lambda _attr: not _attr.startswith('__'),
                                                 dir(class_)))
         )(get_driver(getattr(Provider, provider_name))(provider['auth']['username'], provider['auth']['key']))

        self.node = {
            'size': self.strategy.get_option('hardware', self.list_sizes()),
            'image': self.strategy.get_option('os', self.list_images()),
            'location': self.strategy.get_option('location', self.list_locations())
        }

    def __init__(self, strategy_file=None):
        self.strategy = Strategy(strategy_file)
        self.set_node()

    def restrategise(self):
        self.offset += 1
        self.set_node()


def _build_parser():
    parser = ArgumentParser(description='Deploy/create/manage compute nodes')
    parser.add_argument('-s', '--strategy', help='strategy file [strategy.sample.json]',
                        default=path.join(path.realpath(path.dirname(__file__)), 'config', 'strategy.sample.json'))
    return parser


def main():
    """
    Researching below. Haven't decided on deployment nodes yet; e.g.: might get around to Docker.
    """
    args = _build_parser().parse_args()

    compute = Compute(args.strategy)
    # pp(compute.get_image_names())
    # pp(compute.describe_images())
    # pp(map(lambda c: obj_to_d(c), compute.sizes))

    for i in xrange(len(compute.strategy.strategy['provider']['options'])):  # Threshold
        print 'Attempting to create node on:', compute.strategy.get_provider().keys()[0]
        try:
            print compute.create_node(name='test1', **compute.node)
            break  # Exit loop
        except LibcloudError as e:
            print e.message  # TODO: Use logging module, log this message before continuing
            compute.restrategise()


if __name__ == '__main__':
    main()
