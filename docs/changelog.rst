.. currentmodule:: codingame

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`__.

Version 1.2.0 (unreleased)
--------------------------

Added
*****

- :meth:`Client.get_unread_notifications`.
- :meth:`Client.get_read_notifications`.
- :class:`PartialCodinGamer`.
- :attr:`Notification.codingamer`.
- :attr:`Notification.seen`, :attr:`Notification.seen_date`,
  :attr:`Notification.read` and :attr:`Notification.read_date`.
- :class:`NotificationType` and :class:`NotificationTypeGroup` enums for
  :attr:`Notification.type` and :attr:`Notification.type_group`.
- :class:`NotificationData` and subclasses.

Changed
*******

- Deprecated :attr:`Notification.creation_time` in favor of
  :attr:`Notification.date`

Removed
*******

- ``codingame.endpoints`` submodule.
- ``Notification._raw``.

Version 1.1.0 (2021-11-01)
--------------------------

Changed
*******

- Update :attr:`Client.login` to bypass captcha on login endpoint with
  cookie based authentication, see :ref:`login`.

Version 1.0.1 (2021-07-12)
--------------------------

Added
*****

- :meth:`CodinGamer.profile_url`.

Version 1.0.0 (2021-07-12)
--------------------------

Added
*****

- Asynchronous client with ``Client(is_async=True)``, see :ref:`async`.

- Context managers:

    .. code-block:: python

        # synchronous
        with Client() as client:
            client.get_global_leaderboard()

        #asynchronous
        async with Client(is_async=True) as client:
            await client.get_global_leaderboard()

- More exceptions: :exc:`LoginError` regroups all the exceptions related
  to login: :exc:`LoginRequired`, :exc:`EmailRequired`, :exc:`MalformedEmail`,
  :exc:`PasswordRequired`, :exc:`EmailNotLinked` and :exc:`IncorrectPassword`.
  And :exc:`NotFound` regroups :exc:`CodinGamerNotFound`,
  :exc:`ClashOfCodeNotFound`, :exc:`ChallengeNotFound` and :exc:`PuzzleNotFound`

- :attr:`ChallengeLeaderboard.has_leagues` and
  :attr:`PuzzleLeaderboard.has_leagues`.

- :attr:`Notification._raw`.

Changed
*******

- Remove properties like ``CodinGamer.followers`` in favor of methods like
  :meth:`CodinGamer.get_followers` to better differentiate API calls and to make
  it compatible with async API calls. Here's a list of all of the changed ones:

    - ``Client.language_ids`` -> :meth:`Client.get_language_ids`
    - ``Client.notifications`` ->
      :meth:`Client.get_unseen_notifications`
    - ``CodinGamer.followers`` -> :meth:`CodinGamer.get_followers`
    - ``CodinGamer.followers_ids`` -> :meth:`CodinGamer.get_followers_ids`
    - ``CodinGamer.following`` -> :meth:`CodinGamer.get_followed`
    - ``CodinGamer.following_ids`` -> :meth:`CodinGamer.get_followed_ids`
    - ``CodinGamer.clash_of_code_rank`` ->
      :meth:`CodinGamer.get_clash_of_code_rank`

- Make all attributes of CodinGame models read-only.

- Change type of :attr:`ClashOfCode.time_before_start` and
  :attr:`ClashOfCode.time_before_end` from :class:`float` to
  :class:`datetime.timedelta`.

- Rewrite the way the client works to implement a class to manage the connection
  state and separate the :class:`Client` that the user uses from the HTTP client
  that interacts with the API.

Removed
*******

- Remove argument type validation, not my fault if you can't read the docs.

Version 0.4.0 (2021-06-19)
--------------------------

Added
*****

- :meth:`Client.get_global_leaderboard` with :class:`GlobalLeaderboard` and
  :class:`GlobalRankedCodinGamer`.

- :meth:`Client.get_challenge_leaderboard` with
  :class:`ChallengeLeaderboard`, :class:`ChallengeRankedCodinGamer` and
  :class:`League`.

- :meth:`Client.get_puzzle_leaderboard` with :class:`PuzzleLeaderboard`,
  :class:`PuzzleRankedCodinGamer` and :class:`League`.

Changed
*******

- Update docs style, code style and tests.

Version 0.3.5 (2020-12-10)
--------------------------

Added
*****

- Get a user with their user ID in :meth:`Client.get_codingamer`.

- ``CodinGamer.followers_ids`` and ``CodinGamer.following_ids`` properties to
  get information about followed users and followers without logging in.

- ``CodinGamer.clash_of_code_rank``.

Version 0.3.4 (2020-12-01)
--------------------------

Added
*****

- Support for python 3.9.

Version 0.3.3 (2020-11-06)
--------------------------

Added
*****

- Searching for a CodinGamer with their pseudo in :meth:`Client.get_codingamer`.

- :attr:`CodinGamer.xp`, thanks `@LiJu09 <https://github.com/LiJu09>`__
  (`#3 <https://github.com/takos22/codingame/pull/3>`__).

Version 0.3.2 (2020-09-23)
--------------------------

Added
*****

- :meth:`Client.get_pending_clash_of_code`.

Changed
*******

- Renamed :attr:`Notification.date` to :attr:`Notification.creation_time`.

Version 0.3.1 (2020-09-20)
--------------------------

Added
*****

- ``Client.notifications`` property.

- :class:`Notification` class.

- :exc:`LoginRequired` exception.

Version 0.3.0 (2020-09-20)
--------------------------

Added
*****

- :meth:`Client.login`.

- :meth:`Client.logged_in` and :meth:`Client.codingamer`.

- ``Client.language_ids`` property.

- ``CodinGamer.followers`` and ``CodinGamer.following`` properties.

Version 0.2.1 (2020-09-16)
--------------------------

Added
*****

- Argument type validation.

Version 0.2.0 (2020-09-13)
--------------------------

Added
*****

- :meth:`Client.get_clash_of_code`.

- :class:`ClashOfCode` and :class:`Player` classes.

- :exc:`ClashOfCodeNotFound` exception.

Changed
*******

- Renamed ``Client.codingamer()`` to :meth:`Client.get_codingamer`.

Version 0.1.0 (2020-09-12)
--------------------------

Added
*****

- :class:`Client` class.

- ``Client.codingamer()`` method to get a codingamer.

- :class:`CodinGamer` class.

- :exc:`CodinGamerNotFound` exception.
