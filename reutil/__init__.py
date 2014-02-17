# -*- coding: utf-8 -*-
"""Module for batched multiple text replacements

Copyright (C) 2013  Gregory Vincic

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import codecs
import os
import re
import shutil
import tempfile


class ReDict(object):
    """Replacement dictionary where matched keys are replaced with
    their value.

        >>> from reutil import ReDict
        >>> rd = ReDict({'a ': 'A ', 'ba': 'Ba'})
        >>> txt = "a lonely banana"
        >>> print rd.replace_all(txt)
        A lonely Banana
    """

    def __init__(self, data):
        super(ReDict, self).__init__()
        self.data = data
        self.template = "{value}"

    def _get(self, k):
        """Returns the template rendered value or k if it does not
        exist.
        """
        v = k.group()
        if v in self.data:
            return self.template.format(key=v, value=self.data[v])
        return v

    def replace_all(self, string, template="{value}"):
        """All keys are replaced with their values within the given
        string.

        A template may be given to replace key values with a
        formated variant of the value.

            >>> from reutil import ReDict
            >>> rd = ReDict({'lonely': 'alone'})
            >>> txt = "a lonely banana"
            >>> print rd.replace_all(txt, "{key} -> {value}")
            a lonely -> alone banana
        """

        self.template = template
        for p in self._batch_regexp():
            string = re.sub(p, self._get, string)
        return string

    def _batch_regexp(self):
        patterns = []
        n = 99 # Limitation in sre_compile.py
        data = self.data
        for keygroup in [data.keys()[i:i+n] for i in range(0, len(data), n)]:
            match = ["(%s)" % re.escape(k) for k in keygroup]
            pstr = '|'.join(match)
            pattern = re.compile(pstr)
            patterns.append(pattern)
        return patterns


def msub(patterns_dict, string, template="{value}"):
    """Replaces all keys with values using the given template.

    Returns the replaced string.

        >>> import reutil
        >>> data = {'lonely': 'alone'}
        >>> txt = "a lonely banana"
        >>> template = "{key} -> {value}"
        >>> print reutil.msub(data, txt, template)
        a lonely -> alone banana
    """
    rd = ReDict(patterns_dict)
    return rd.replace_all(string, template)

def msub_in(patterns_dict, path, template="{value}", encoding="utf-8"):
    """Same as msub but replaces the given file with the replaced
    one.

    Creates temporary files inside the directory of the given path.

        >>> import reutil
        >>> out = open("test.txt", "w")
        >>> out.write("a lonely banana")
        >>> out.close()
        >>> data = {'lonely': 'alone'}
        >>> template = "{key} -> {value}"
        >>> reutil.msub_in(data, "test.txt", template)
        >>> print open("test.txt", 'r').read()
        a lonely -> alone banana
    """
    dpath = os.path.dirname(path)
    out_path = tempfile.mktemp(dir=dpath)
    with codecs.open(path, 'r', encoding) as in_fh:
        with codecs.open(out_path, "w", encoding) as out_fh:
            for line in in_fh:
                rline = msub(patterns_dict, line, template)
                out_fh.write(rline)
    shutil.copyfile(out_path, path)
    os.remove(out_path)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
