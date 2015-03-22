from os import environ
from string import whitespace

_quotes = set("'\"")
_whitespace_or_quotes = set(whitespace + "'\"")
_whitespace_or_quotes_or_brace = set(whitespace + "'\"}{")


def _strip_stack(_stack, run_before=False):
    if len(_stack) > 1 and _stack[0] in _whitespace_or_quotes_or_brace:
        del _stack[0]
    if len(_stack) > 1 and _stack[-1] in _whitespace_or_quotes_or_brace:
        del _stack[-1]
    if not run_before:
        return _strip_stack(_stack, True)


def _handle_env(_res, _stack):
    """ If the environment variable can't be resolved, key error isn't raised.
    To raise KeyError replace `environ.get(env, env)` with `environ[env]`
    """
    if not _stack:
        return _res

    _strip_stack(_stack)

    (lambda s: s.startswith('env.') and (
        lambda env: _res.append((env, environ.get(env[len('env.'):], env))))(''.join(_stack)))(''.join(_stack))
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
