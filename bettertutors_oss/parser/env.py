from os import environ
from string import whitespace, punctuation

_quotes = set("'\"")
_whitespace_or_punctuation = set(whitespace + ''.join(c for c in punctuation if c not in ('.', '_')))


def _handle_env(_res, _stack):
    """ If the environment variable can't be resolved, key error isn't raised.
    To raise KeyError replace `environ.get(env, env)` with `environ[env]`
    """
    if not _stack:
        return _res

    (lambda env: (
        lambda find: find != -1 and (lambda _env: _res.append((_env, environ.get(_env[len('env.'):], _env))))(
            ''.join(c for c in env[find:] if c not in _whitespace_or_punctuation)
        )
    )(env.find('env.')))(''.join(_stack))
    del _stack[:]
    return _res


def _handle_c(c, _res=[], _stack=[]):
    _handle_env(_res, _stack) if c in whitespace else _stack.append(c)


def parse_out_env(_line):
    _res, _stack = [], []

    for c in _line:
        _handle_c(c, _res, _stack)
    _handle_env(_res, _stack)

    return reduce(lambda a, kv: a.replace(*kv), _handle_env(_res, _stack), _line)
