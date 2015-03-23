# Will I ever get back to this? :P

from collections import MutableMapping
from easydict import EasyDict


class Strategy(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = EasyDict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __getattr__(self, item):
        return self.store[item]

    def __delattr__(self, item):
        return self.__delitem__(item)

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
