.. module:: codingame
    :synopsis: Wrapper for the undocumented CodinGame API.

codingame |version| API Reference
=================================

The following section outlines the API of the ``codingame`` module. All the
public classes, methods and functions are documented here.

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

Hybrid client
*************

.. autoclass:: Client

Synchronous client
******************

.. autoclass:: codingame.client.sync.SyncClient

.. currentmodule:: codingame

Asynchronous client
*******************

.. autoclass:: codingame.client.async_.AsyncClient

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
**********

.. autoclass:: PartialCodinGamer()

.. autoclass:: CodinGamer()

Clash of Code
*************

.. autoclass:: ClashOfCode()

.. autoclass:: Player()

Notification
************

.. autoclass:: Notification()

Enumerations
############

.. autoclass:: NotificationTypeGroup()
    :undoc-members:

.. autoclass:: NotificationType()
    :undoc-members:

Notification data
#################

These are typing annotations for :attr:`Notification.data`

.. autotypeddict:: codingame.types.FriendRegisteredData()
.. autotypeddict:: codingame.types.notification._ContestData()
.. autotypeddict:: codingame.types.ContestScheduledData()
.. autotypeddict:: codingame.types.ContestSoonData()
.. autotypeddict:: codingame.types.ContestStartedData()
.. autotypeddict:: codingame.types.ContestOverData()
.. autotypeddict:: codingame.types.notification._ContributionData()
.. autotypeddict:: codingame.types.notification._PuzzleSolutionData()
.. autotypeddict:: codingame.types.notification._NewCommentData()
.. autotypeddict:: codingame.types.notification._CompleteNewCommentData()
.. autotypeddict:: codingame.types.notification._URLNewCommentData()

.. class:: codingame.types.notification.NewCommentData()

    alias of :class:`codingame.types.notification._CompleteNewCommentData` or
    :class:`codingame.types.notification._URLNewCommentData`

.. class:: codingame.types.notification.NewCommentResponseData()

    alias of :class:`codingame.types.notification._CompleteNewCommentData` or
    :class:`codingame.types.notification._URLNewCommentData`

.. autotypeddict:: codingame.types.notification.ClashInviteData()
.. autotypeddict:: codingame.types.notification.ClashOverData()
.. autotypeddict:: codingame.types.notification.AchievementUnlockedData()
.. autotypeddict:: codingame.types.notification.NewLevelData()
.. autotypeddict:: codingame.types.notification.NewBlogData()
.. autotypeddict:: codingame.types.notification.FeatureData()
.. autotypeddict:: codingame.types.notification._LeagueData()
.. autotypeddict:: codingame.types.notification.NewLeagueData()
.. autotypeddict:: codingame.types.notification.ElligibleForNextLeagueData()
.. autotypeddict:: codingame.types.notification.ContributionReceivedData()
.. autotypeddict:: codingame.types.notification.ContributionAcceptedData()
.. autotypeddict:: codingame.types.notification.ContributionRefusedData()
.. autotypeddict:: codingame.types.notification.ContributionClashModeRemovedData()
.. autotypeddict:: codingame.types.notification.NewPuzzleData()
.. autotypeddict:: codingame.types.notification.PuzzleOfTheWeekData()
.. autotypeddict:: codingame.types.notification.NewLeagueOpenedData()
.. autotypeddict:: codingame.types.notification.NewHintData()
.. autotypeddict:: codingame.types.notification.ContributionModeratedData()
.. autotypeddict:: codingame.types.notification.QuestCompletedData()
.. autotypeddict:: codingame.types.notification._GenericData()
.. autotypeddict:: codingame.types.notification.InfoGenericData()
.. autotypeddict:: codingame.types.notification.WarningGenericData()
.. autotypeddict:: codingame.types.notification.ImportantGenericData()
.. autotypeddict:: codingame.types.notification.CustomData()

Leaderboards
************

Global leaderboard
##################

.. autoclass:: GlobalRankedCodinGamer()

.. autoclass:: GlobalLeaderboard()

Challenge leaderboard
#####################

.. autoclass:: League()

.. autoclass:: ChallengeRankedCodinGamer()

.. autoclass:: ChallengeLeaderboard()

Puzzle leaderboard
##################

.. autoclass:: PuzzleRankedCodinGamer()

.. autoclass:: PuzzleLeaderboard()

Exceptions
----------

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
*******************

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
