#!/usr/bin/env python

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from parse_strategy import parse_strategy
from utils import pp


def get_images_and_sizes(strategy_file=None):
    strategy = parse_strategy(strategy_file)
    conn = get_driver(getattr(Provider, strategy['provider']))(strategy['auth']['username'],
                                                               strategy['auth']['key'])
    # Generate API key from users view in the online dashboard

    images = conn.list_images()
    sizes = conn.list_sizes()

    return images, sizes


get_image_names = lambda images: map(lambda image: image.name, images)
describe_images = lambda images: map(
    lambda image: {k: (lambda call: call() if hasattr(call, '__call__') else call)(getattr(image, k))
                   for k in filter(lambda k: not k.startswith('_'), dir(image))}, images)


def main():
    """
    Researching below. Haven't decided on deployment nodes yet; e.g.: might get around to Docker.
    """
    images, sizes = get_images_and_sizes()
    print 'images =', images, '\nsizes=', sizes
    ubuntus = filter(lambda image: 'Ubuntu' in image.name, images)
    pp(describe_images(ubuntus))
    pp(get_image_names(images))

    pp(filter(lambda k: not k.startswith('_'), dir(ubuntus[0])))


if __name__ == '__main__':
    main()
