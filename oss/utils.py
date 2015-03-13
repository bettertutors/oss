from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

unroll_d = lambda d, *keys: (d[key] for key in keys)
