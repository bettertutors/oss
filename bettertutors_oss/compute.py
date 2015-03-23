#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from collections import Callable

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from parse_strategy import parse_strategy
from utils import pp, obj_to_d


class Compute(object):
    """ Light wrapper around libcloud to facilitate integration with strategy files,
        and simplification of commands """

    def __init__(self, strategy_file=None):
        self.strategy = parse_strategy(strategy_file)

        self.conn = get_driver(getattr(Provider, self.strategy['provider']['primary']['name']))(
            self.strategy['provider']['primary']['auth']['username'],
            self.strategy['provider']['primary']['auth']['key']
        )
        # TODO: Inherit from `conn`

        self.images = self.conn.list_images()
        self.sizes = self.conn.list_sizes()

        self.node = {
            'size': filter(lambda size: size.name == self.strategy['node']['hardware']['name'],
                           self.sizes)[0],
            'image': filter(
                lambda image: image.name == self.strategy['node']['os']['name'],
                self.images)[0],
            'location': filter(
                lambda location: location.name == self.strategy['node']['location']['name'],
                self.conn.list_locations())[0]
        }

    get_image_names = lambda self: map(lambda image: image.name, self.images)
    get_image_names.__doc__ = '@returns [\'CentOS - Latest\', \'Ubuntu - Latest\', ...]'

    describe_images = lambda self: map(
        lambda image: {k: (lambda val: val() if isinstance(val, Callable) else val)(v)
                       for k, v in obj_to_d(image).iteritems()},
        self.images
    )
    describe_images.__doc__ = """@returns [{'driver': <libcloud.compute.drivers.softlayer.SoftLayerNodeDriver>,
                                            'extra': {}, 'id': 'CENTOS_LATEST', 'name': 'CentOS - Latest',
                                            'get_uuid': 'bdf9042e52df724f43c4129ec91995ece796604c',
                                            'uuid': 'bdf9042e52df724f43c4129ec91995ece796604c'}, ...]"""


def _build_parser():
    parser = ArgumentParser(description='Deploy/create/manage compute nodes')
    parser.add_argument('-s', '--strategy', help='strategy file',
                        default=path.join(path.realpath(path.dirname(__file__)), 'config', 'strategy.sample.json'))
    return parser


def main():
    """
    Researching below. Haven't decided on deployment nodes yet; e.g.: might get around to Docker.
    """
    args = _build_parser().parse_args()
    print 'args.strategy =', args.strategy

    compute = Compute(args.strategy)
    # pp(compute.get_image_names())
    # pp(compute.describe_images())
    # pp(map(lambda c: obj_to_d(c), compute.sizes))

    print compute.conn.create_node(name='test1', **compute.node)


if __name__ == '__main__':
    main()
