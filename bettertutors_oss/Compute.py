#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from time import sleep

from libcloud.compute.types import Provider, LibcloudError
from libcloud.compute.providers import get_driver
from libcloud import security

from Strategy import Strategy
from utils import pp, obj_to_d, find_one

# AWS Certificates are acting up, remove this in production:
security.VERIFY_SSL_CERT = False


class Compute(object):
    """ Light wrapper around libcloud to facilitate integration with strategy files,
        and simplification of commands """

    offset = 0
    node_specs = None
    node = None
    provider_name = None
    provider_dict = None
    provider_cls = None
    key_pair = None

    def __init__(self, strategy_file):
        self.strategy = Strategy(strategy_file)
        self.set_node()

    def __getattr__(self, item):
        return getattr(self.provider_cls, item)

    def set_node(self):
        self.provider_name, self.provider_dict = (
            lambda _provider_obj: (lambda name: (name, _provider_obj[name]))(_provider_obj.keys()[0])
        )(self.strategy.get_provider(self.offset))

        self.provider_cls = get_driver(getattr(Provider, self.provider_name))(self.provider_dict['auth']['username'],
                                                                              self.provider_dict['auth']['key'])

        self.node_specs = {
            'size': self.strategy.get_option('hardware', self.list_sizes()),
            'image': self.strategy.get_option('image', self.list_images()),
            'location': self.strategy.get_option('location', self.list_locations())
        }
        if 'security_group' in self.provider_dict:
            self.node_specs.update({'ex_securitygroup': self.provider_dict['security_group']})
        if 'key_name' in self.provider_dict:
            self.node_specs.update({'ex_keyname': self.provider_dict['key_name']})

    def restrategise(self):
        self.offset += 1
        self.set_node()

    def setup_keypair(self):
        try:
            self.import_key_pair_from_file(
                name=self.provider_dict['ssh']['key_name'],
                key_file_path=self.provider_dict['ssh']['public_key_path']
            )
        except Exception as e:
            if not e.message.startswith('InvalidKeyPair.Duplicate'):
                raise e

    def provision(self):
        for i in xrange(len(self.strategy.strategy['provider']['options'])):  # Threshold
            print 'Attempting to create node on:', self.provider_name
            try:
                if self.provider_name != 'SOFTLAYER':
                    self.setup_keypair()
                    self.node = self.create_node(name='test1', **self.node_specs)

                    threshold = 60
                    print 'Waiting [up to] 10 minutes for node to come online'
                    PENDING = 3  # Where do I find the enum?!
                    while threshold and self.node.state == PENDING:
                        sleep(10)
                        threshold -= 1
                        print 'Waiting another:', threshold * 10, 'seconds. Status is:', self.node.extra['status']
                    if self.node.state != PENDING:
                        print 'self.node.state =', self.node.state, "self.node.extra['status'] =", self.node.extra['status']
                        return self.node
                    else:
                        pass
                        # Maybe kill the node here before going off with next provider?
                else:
                    pass
                    # Having issues with SoftLayer billing at the moment, will remove condition once resolved.
            except LibcloudError as e:
                print e.message, '\n'  # TODO: Use logging module, log this message before continuing

            self.restrategise()
        raise LibcloudError('Failed to provision node')


def _build_parser():
    parser = ArgumentParser(description='Deploy/create/manage compute nodes')
    parser.add_argument('-s', '--strategy', help='strategy file [strategy.sample.json]',
                        default=path.join(path.realpath(path.dirname(__file__)), 'config', 'strategy.sample.json'))
    return parser


def main():
    args = _build_parser().parse_args()
    compute = Compute(args.strategy)
    print compute.provision()


if __name__ == '__main__':
    main()
