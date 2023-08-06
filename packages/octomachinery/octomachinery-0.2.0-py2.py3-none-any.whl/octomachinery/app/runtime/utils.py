"""GitHub App runtime context helpers."""

from contextvars import ContextVar, Token
import logging
import os
import typing


logger = logging.getLogger(__name__)


class ContextLookupError(AttributeError):
    """Context var lookup error."""


class _ContextMap:
    __slots__ = '__map__', '__token_map__'

    def __init__(self, **initial_vars):
        self.__map__: typing.Dict[str, ContextVar[typing.Any]] = {
            k: ContextVar(v) for k, v in initial_vars.items()
        }
        """Storage for all context vars."""

        self.__token_map__: typing.Dict[str, Token[typing.Any]] = {}
        """Storage for individual context var reset tokens."""

    def __dir__(self):
        """Render a list of public attributes."""
        return self.__map__.keys()

    def __getattr__(self, name):
        if name in ('__map__', '__token_map__'):
            return getattr(self, name)
        try:
            return self.__map__[name].get()
        except LookupError:
            raise ContextLookupError(f'No `{name}` present in the context')

    def __setattr__(self, name, value):
        if name in ('__map__', '__token_map__'):
            object.__setattr__(self, name, value)
        elif name in self.__map__:
            reset_token = self.__map__[name].set(value)
            self.__token_map__[name] = reset_token
        else:
            raise ContextLookupError(f'No `{name}` present in the context')

    def __delattr__(self, name):
        if name not in self.__map__:
            raise ContextLookupError(f'No `{name}` present in the context')
        reset_token = self.__token_map__[name]
        self.__map__[name].reset(reset_token)
        del self.__token_map__[name]


def detect_env_mode():
    """Figure out whether we're under GitHub Action environment."""
    for var_suffix in {
            'WORKFLOW',
            'ACTION', 'ACTOR',
            'REPOSITORY',
            'EVENT_NAME', 'EVENT_PATH',
            'WORKSPACE',
            'SHA', 'REF',
            'TOKEN',
    }:
        if f'GITHUB_{var_suffix}' not in os.environ:
            logger.info(
                'Detected GitHub App mode since '
                'GITHUB_%s is missing from the env',
                var_suffix,
            )
            return 'app'
    logger.info(
        'Detected GitHub Action mode since all the '
        'typical env vars are present in the env',
    )
    return 'action'
