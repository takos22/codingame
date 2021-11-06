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

.. autoclass:: ContributionType()
    :undoc-members:

.. autoclass:: CommentType()
    :undoc-members:

.. autoclass:: ContributionModeratedActionType()
    :undoc-members:

Notification data
#################

.. autoclass:: LanguageMapping()
    :no-inherited-members:

.. autoclass:: NotificationData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: AchievementUnlockedData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: LeagueData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewBlogData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: ClashInviteData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: ClashOverData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: Contribution()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: PuzzleSolution()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewCommentData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewCommentResponseData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: ContributionData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: FeaturedData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewHintData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: ContributionModeratedData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewPuzzleData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: PuzzleOfTheWeekData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: QuestCompletedData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: FriendRegisteredData()
    :undoc-members:
    :no-inherited-members:

.. autoclass:: NewLevelData()
    :undoc-members:
    :no-inherited-members:

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

.. autoexception:: WrongCaptchaAnswer

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
            - :exc:`WrongCaptchaAnswer`
            - :exc:`LoginRequired`
        - :exc:`NotFound`
            - :exc:`CodinGamerNotFound`
            - :exc:`ClashOfCodeNotFound`
            - :exc:`ChallengeNotFound`
            - :exc:`PuzzleNotFound`
