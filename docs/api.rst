.. currentmodule:: codingame

=============
API Reference
=============

The following section outlines the API of codingame.

Version Related Info
--------------------

There are two main ways to query version information about the library.

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of :pep:`440`.

Client
------

.. autoclass:: Client
    :members:
    :inherited-members:

.. autoclass:: codingame.client.sync.SyncClient()
    :members:
    :inherited-members:

.. autoclass:: codingame.client.async_.AsyncClient()
    :members:
    :inherited-members:

.. currentmodule:: codingame

.. _codingame_api_models:

CodinGame Models
----------------

Models are classes that are created from the data received from CodinGame and
are not meant to be created by the user of the library.

.. danger::

    The classes listed below are **not intended to be created by users** and are
    also **read-only**.

    For example, this means that you should not make your own
    :class:`CodinGamer` instances nor should you modify the :class:`CodinGamer`
    instance yourself.


CodinGamer
~~~~~~~~~~~~

.. autoclass:: CodinGamer()

Clash of Code
~~~~~~~~~~~~~~~

.. autoclass:: ClashOfCode()

.. autoclass:: Player()

Notification
~~~~~~~~~~~~

.. autoclass:: Notification()

Leaderboards
~~~~~~~~~~~~

Global leaderboard
******************

.. autoclass:: GlobalRankedCodinGamer()
    :inherited-members:

.. autoclass:: GlobalLeaderboard()
    :inherited-members:

Challenge leaderboard
*********************

.. autoclass:: League()

.. autoclass:: ChallengeRankedCodinGamer()
    :inherited-members:

.. autoclass:: ChallengeLeaderboard()
    :inherited-members:

Puzzle leaderboard
******************

.. autoclass:: PuzzleRankedCodinGamer()
    :inherited-members:

.. autoclass:: PuzzleLeaderboard()
    :inherited-members:

Exceptions
------------

The following exceptions are thrown by the library.

.. autoexception:: CodinGameAPIError

.. autoexception:: LoginError

.. autoexception:: EmailRequired

.. autoexception:: MalformedEmail

.. autoexception:: PasswordRequired

.. autoexception:: EmailNotLinked

.. autoexception:: IncorrectPassword

.. autoexception:: LoginRequired

.. autoexception:: NotFound

.. autoexception:: CodinGamerNotFound

.. autoexception:: ClashOfCodeNotFound

.. autoexception:: ChallengeNotFound

.. autoexception:: PuzzleNotFound

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~~~

- :exc:`Exception`
    - :exc:`CodinGameAPIError`
        - :exc:`LoginError`
            - :exc:`EmailRequired`
            - :exc:`MalformedEmail`
            - :exc:`PasswordRequired`
            - :exc:`EmailNotLinked`
            - :exc:`IncorrectPassword`
            - :exc:`LoginRequired`
        - :exc:`NotFound`
            - :exc:`CodinGamerNotFound`
            - :exc:`ClashOfCodeNotFound`
            - :exc:`ChallengeNotFound`
            - :exc:`PuzzleNotFound`
