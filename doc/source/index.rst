reutil
======

*Module for batched multiple text replacements.*

The purpose of this module is to make it easier for developers
to do multiple replacements in text and files with basic python
knowledge.


Example
-------


    >>> import reutil
    >>> out = open("test.txt", "w")
    >>> out.write("""I like fruit
    ... I love apples
    ... I hate beans""")
    >>> out.close()
    >>> patterns_dict = {'apples': 'oranges', 'beans': 'darth vader'}
    >>> template = "{key} and {value}"
    >>> reutil.msub_in(patterns_dict, "test.txt", template)
    >>> print open("test.txt", 'r').read()
    I like fruit
    I love apples and oranges
    I hate beans and darth vader


API
---

.. toctree::
   :maxdepth: 1

   reutil

