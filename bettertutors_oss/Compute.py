#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from time import sleep

from libcloud.compute.types import Provider, LibcloudError
from libcloud.compute.providers import get_driver
from libcloud import security
from libcloud.compute.deployment import SSHKeyDeployment

from Strategy import Strategy
from utils import pp, obj_to_d, find_one, ping_port

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

    def __getattr__(self, attr):
        return getattr(self.provider_cls, attr)

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

    def provision(self, create_or_deploy='create'):
        for i in xrange(len(self.strategy.strategy['provider']['options'])):  # Threshold
            print 'Attempting to create node on:', self.provider_name
            try:
                if self.provider_name != 'SOFTLAYER':
                    self.setup_keypair()
                    if create_or_deploy == 'deploy':
                        with open(self.provider_dict['ssh']['public_key_path'], mode='rt') as f:
                            ssh_key = f.read()
                        self.node_specs.update({'deploy': SSHKeyDeployment(ssh_key)})
                    try:
                        self.node = getattr(self, '{0}_node'.format(create_or_deploy))(name='test1', **self.node_specs)
                    except NotImplementedError as e:
                        error_message = 'deploy_node not implemented for this driver'
                        if e.message != error_message:
                            raise
                        print '{error_message}, so running `create_node` instead.'.format(
                            error_message=error_message.replace('deploy_node', '`deploy_node`')
                        )
                        self.node = self.create_node(name='test1', **self.node_specs)
                    try:
                        return self.wait_until_running([self.node])
                    except LibcloudError as e:
                        print e.message, '\n'  # TODO: Use logging module, log this message before continuing
                        # Maybe kill the node here before going off with next provider?
                        pass
                else:
                    # Having issues with SoftLayer billing at the moment, will remove condition once resolved.
                    pass
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
    print compute.provision('deploy')


if __name__ == '__main__':
    main()
