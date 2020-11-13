from functools import cached_property

from loguru import logger


class UserStats(object):
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
            'class',
        ]

    @cached_property
    def userclass(self):
        return self._dictionary['class']
