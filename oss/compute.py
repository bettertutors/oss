#!/usr/bin/env python

from os import path
from argparse import ArgumentParser

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from parse_strategy import parse_strategy
from utils import pp


class Compute(object):
    """ Light wrapper around libcloud to facilitate integration with strategy files,
        and simplification of commands """

    def __init__(self, strategy_file=None):
        self.strategy = parse_strategy(strategy_file)

        self.conn = get_driver(getattr(Provider, self.strategy['provider']))(self.strategy['auth']['username'],
                                                                             self.strategy['auth']['key'])

        self.images = self.conn.list_images()
        self.sizes = self.conn.list_sizes()

    get_image_names = lambda self: map(lambda image: image.name, self.images)
    get_image_names.__doc__ = '@returns [\'CentOS - Latest\', \'Ubuntu - Latest\', ...]'

    describe_images = lambda self: map(
        lambda image: {k: (lambda call: call() if hasattr(call, '__call__') else call)(getattr(image, k))
                       for k in filter(lambda k: not k.startswith('_'), dir(image))}, self.images
    )
    describe_images.__doc__ = """@returns [{'driver': <libcloud.compute.drivers.softlayer.SoftLayerNodeDriver>,
                                            'extra': {}, 'id': 'CENTOS_LATEST', 'name': 'CentOS - Latest',
                                            'get_uuid': 'bdf9042e52df724f43c4129ec91995ece796604c',
                                            'uuid': 'bdf9042e52df724f43c4129ec91995ece796604c'}, ...]"""


def _build_parser():
    parser = ArgumentParser(description='Deploy/create/manage compute nodes')
    parser.add_argument('-s', '--strategy', help='strategy file',
                        default=path.join(path.dirname(__file__), 'strategy.json'))
    return parser


def main():
    """
    Researching below. Haven't decided on deployment nodes yet; e.g.: might get around to Docker.
    """
    args = _build_parser().parse_args()

    compute = Compute(args.strategy)
    pp(compute.get_image_names())
    pp(compute.describe_images())

    pp(filter(lambda k: not k.startswith('_'), dir(compute.images[0])))


if __name__ == '__main__':
    main()
