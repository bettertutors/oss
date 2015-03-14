#!/usr/bin/env python

from os import environ
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


def main():
    Driver = get_driver(Provider.SOFTLAYER)
    conn = Driver(environ['SL_USER'], environ['SL_KEY'])
    # Generate API key from users view in the online dashboard

    # retrieve available images and sizes
    images = conn.list_images()
    # [<NodeImage: id=3, name=Gentoo 2008.0, driver=Rackspace  ...>, ...]
    sizes = conn.list_sizes()
    # [<NodeSize: id=1, name=256 server, ram=256 ... driver=Rackspace .

    return locals()


if __name__ == '__main__':
    """
    Researching below. Haven't decided on deployment nodes yet; e.g.: might get around to Docker.
    """
    lc = main()
    print 'images =', lc['images'], '\nsizes=', lc['sizes']
    ubuntus = filter(lambda image: 'Ubuntu' in image.name, lc['images'])
    pp(map(lambda image: {k: (lambda call: call() if hasattr(call, '__call__') else call)(getattr(image, k))
                          for k in filter(lambda k: not k.startswith('_'), dir(image))}, ubuntus))
    pp(filter(lambda k: not k.startswith('_'), dir(ubuntus[0])))
