.. currentmodule:: codingame

===============
API Reference
===============

The following section outlines the API of codingame.

Version Related Info
----------------------

There are two main ways to query version information about the library.

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of :pep:`440`.

Client
--------

.. autoclass:: Client()
    :members:


.. _codingame_api_models:

CodinGame Models
------------------

Models are classes that are received from CodinGame and are not meant to be created by
the user of the library.

.. danger::

    The classes listed below are **not intended to be created by users** and are also
    **read-only**.

    For example, this means that you should not make your own :class:`CodinGamer` instances
    nor should you modify the :class:`CodinGamer` instance yourself.


CodinGamer
~~~~~~~~~~~~

.. autoclass:: CodinGamer()
    :members:

Clash of Code
~~~~~~~~~~~~~~~

.. autoclass:: ClashOfCode()
    :members:

.. autoclass:: Player()
    :members:

Exceptions
------------

The following exceptions are thrown by the library.

.. autoexception:: CodinGameAPIError

.. autoexception:: CodinGamerNotFound

.. autoexception:: ClashOfCodeNotFound

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~~~

- :exc:`Exception`
    - :exc:`CodinGameAPIError`
        - :exc:`CodinGamerNotFound`
        - :exc:`ClashOfCodeNotFound`
