from collections import MutableMapping


class Strategy(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __getattr__(self, item):
        return self.store[item]

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


if __name__ == '__main__':
    strategy = Strategy(a=5, b=6)
    print 'strategy.a =', strategy.a
    del strategy.a
    print 'strategy.a =', strategy.a
