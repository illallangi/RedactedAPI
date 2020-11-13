from functools import cached_property

from loguru import logger

from .userstats import UserStats


class Index(object):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                logger.error(f'Unhandled key in {self.__class__}: {key}: {type(self._dictionary[key])}"{self._dictionary[key]}"')
                continue
            logger.trace(f'{key}: {type(self._dictionary[key])}"{self._dictionary[key]}"')

    @property
    def _keys(self):
        return [
            'username',
            'userstats',
        ]

    def __repr__(self):
        return f'{self.__class__}{self.username} ({self.userstats.userclass})'

    def __str__(self):
        return f'{self.username} ({self.userstats.userclass})'

    @cached_property
    def username(self):
        return self._dictionary['username']

    @cached_property
    def userstats(self):
        return UserStats(self._dictionary['userstats'])
