#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from collections import Callable

from libcloud.compute.types import Provider, LibcloudError
from libcloud.compute.providers import get_driver

from Strategy import Strategy
from utils import pp, obj_to_d


class Compute(object):
    """ Light wrapper around libcloud to facilitate integration with strategy files,
        and simplification of commands """

    offset = 0

    def init(self):
        provider_name, provider = (
            lambda _provider_obj: (lambda name: (name, _provider_obj[name]))(_provider_obj.keys()[0])
        )(self.strategy.get_provider(self.offset))

        conn = get_driver(getattr(Provider, provider_name))(provider['auth']['username'], provider['auth']['key'])
        # TODO: Inherit from `conn`
        images = conn.list_images()
        sizes = conn.list_sizes()
        node = {
            'size': filter(lambda size: size.name == self.strategy.get_hardware(), sizes)[0],
            'image': filter(lambda image: image.name == self.strategy.get_os()['name'], images)[0],
            'location': filter(
                lambda location: location.name == self.strategy.get_location()['name'], conn.list_locations())[0]
        }

        return conn, images, sizes, node

    def __init__(self, strategy_file=None):
        self.strategy = Strategy(strategy_file)
        self.conn, self.images, self.sizes, self.node = self.init()

    def restrategise(self):
        self.offset += 1
        self.conn, self.images, self.sizes, self.node = self.init()

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

    compute = Compute(args.strategy)
    # pp(compute.get_image_names())
    # pp(compute.describe_images())
    # pp(map(lambda c: obj_to_d(c), compute.sizes))

    for i in xrange(len(compute.strategy.strategy['provider']['options'])):  # Threshold
        try:
            print compute.conn.create_node(name='test1', **compute.node)
            break  # Exit loop
        except LibcloudError as e:
            print e.message  # TODO: Use logging module, log this message before continuing
            compute.restrategise()


if __name__ == '__main__':
    main()
