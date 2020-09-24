# -*- coding: utf-8 -*-
#
#  Copyright 2020 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of CompressShelve.
#
#  CompressShelve is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from shelve import DbfilenameShelf
from compress_pickle import dumps, loads


class CompressShelve(DbfilenameShelf):
    def __init__(self, filename, flag='c', protocol=-1, writeback=False, compression='gzip', fix_imports=True,
                 buffer_callback=None, buffers=None, optimize=True, encoding='ASCII', errors='strict', arcname=None,
                 **kwargs):
        """
        Params description see in shelve.open and compress_pickle loads and dumps functions.
        """
        super().__init__(filename, flag, protocol, writeback)
        self._compression = compression
        self._fix_imports = fix_imports
        self._buffer_callback = buffer_callback
        self._buffers = buffers
        self._optimize = optimize
        self._encoding = encoding
        self._errors = errors
        self._arcname = arcname
        self._kwargs = kwargs

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            value = loads(self.dict[key.encode(self.keyencoding)], self._compression, self._fix_imports,
                          self._encoding, self._errors, self._buffers, arcname=self._arcname, **self._kwargs)
            if self.writeback:
                self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        if self.writeback:
            self.cache[key] = value
        self.dict[key.encode(self.keyencoding)] = dumps(value, self._compression, self._protocol, self._fix_imports,
                                                        self._buffer_callback, self._optimize, **self._kwargs)


__all__ = ['CompressShelve']
