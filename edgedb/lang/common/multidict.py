##
# Copyright (c) 2008-2010 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##

import collections


_NoDefault = object()


class Multidict(collections.UserDict):

    def __init__(self, data=None):
        if isinstance(data, dict):
            self.data = collections.OrderedDict(
                (key, self._cast_to_list(value))
                for key, value in data.items())

        elif isinstance(data, collections.Iterable):
            self.data = collections.OrderedDict()
            for key, value in data:
                getattr(
                    self.data.setdefault(key, []), 'extend'
                    if self._is_iterable(value) else 'append')(value)

        elif data:
            raise TypeError('Invalid data to initialize MultiDict')

        else:
            self.data = collections.OrderedDict()

    def _is_iterable(self, value):
        return isinstance(value, (list, tuple))

    def _cast_to_list(self, value, copy=False):
        if isinstance(value, list):
            return value[:]
        else:
            return list(value) if self._is_iterable(value) else [value]

    def __getitem__(self, key):
        if key in self.data:
            return self.data.__getitem__(key)[0]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.data[key] = self._cast_to_list(value)

    def add(self, key, value):
        if key in self.data:
            self.data[key].append(value)
        else:
            self.data[key] = [value]

    def getlist(self, key, default=None):
        if key in self.data:
            return self.data[key]

        if default is not None:
            return self._cast_to_list(default)
        return default

    def setdefault(self, key, value):
        try:
            return self.data[key]
        except KeyError:
            self.data[key] = value
            return self.data[key]

    def pop(self, key, default=_NoDefault):
        if key in self.data:
            item = self.data[key][0]
            del self.data[key][0]

            if not self.data[key]:
                del self.data[key]

            return item

        if default is not _NoDefault:
            return default

        raise KeyError(key)

    def itemlists(self):
        for key in self.data:
            yield key, self.data[key]