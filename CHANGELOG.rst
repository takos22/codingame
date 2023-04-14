Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`__.

Version 1.4.2 (2023-04-14)
--------------------------

Fixed
*****

- `KeyError <https://docs.python.org/library/exceptions.html#KeyError>`__ was raised when using `Client.get_challenge_leaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_challenge_leaderboard>`__
  instead of `NotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotFound>`__ because of an API change by CodinGame.

Version 1.4.1 (2023-02-11)
--------------------------

Fixed
*****

- `ValueError <https://docs.python.org/library/exceptions.html#ValueError>`__ when using `Client.get_pending_clash_of_code <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_pending_clash_of_code>`__ because
  of a change in datetime format by CodinGame.

Version 1.4.0 (2022-08-19)
--------------------------

Added
*****

- `Client.mark_notifications_as_seen <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.mark_notifications_as_seen>`__ and
  `Client.mark_notifications_as_read <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.mark_notifications_as_read>`__.
- `Notification.mark_as_seen <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.mark_as_seen>`__ and `Notification.mark_as_read <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.mark_as_read>`__.

Removed
*******

- Removed support for python 3.6 as it has reached its end of life. For more
  information, see `PEP 494 <https://peps.python.org/pep-0494/#lifespan>`__.

Version 1.3.0 (2022-06-21)
--------------------------

Added
*****

- `Client.get_unread_notifications <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_unread_notifications>`__.
- `Client.get_read_notifications <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_read_notifications>`__.
- `PartialCodinGamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.PartialCodinGamer>`__.
- `Notification.codingamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.codingamer>`__.
- `Notification.seen <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.seen>`__, `Notification.seen_date <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.seen_date>`__,
  `Notification.read <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.read>`__ and `Notification.read_date <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.read_date>`__.
- `NotificationType <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotificationType>`__ and `NotificationTypeGroup <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotificationTypeGroup>`__ enums for
  `Notification.type <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.type>`__ and `Notification.type_group <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.type_group>`__.
- `NotificationData <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotificationData>`__ and subclasses.

Changed
*******

- Deprecated `Notification.creation_time <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.creation_time>`__ in favor of
  `Notification.date <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.date>`__

Removed
*******

- Removed `Notification._raw`.

Version 1.2.4 (2022-06-17)
--------------------------

Fixed
*****

- `CodinGamer.get_followers <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followers>`__ and `CodinGamer.get_followed <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followed>`__ now work
  while being logged in as any user, not just as the user you want to get the
  followers of.

Version 1.2.3 (2021-11-07)
--------------------------

Fixed
*****

- `ImportError <https://docs.python.org/library/exceptions.html#ImportError>`__ of ``codingame.types`` submodule when importing
  ``codingame``, the ``1.2.1`` and ``1.2.2`` fixes don't work.

Version 1.2.2 (2021-11-06)
--------------------------

Fixed
*****

- `ImportError <https://docs.python.org/library/exceptions.html#ImportError>`__ of ``codingame.types`` submodule when importing
  ``codingame``.

Version 1.2.1 (2021-11-06)
--------------------------

Fixed
*****

- `ModuleNotFoundError <https://docs.python.org/library/exceptions.html#ModuleNotFoundError>`__ of ``codingame.types`` submodule when importing
  ``codingame``.

Version 1.2.0 (2021-11-04)
--------------------------

Added
*****

- `Client.request <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.request>`__ to make requests to CodinGame API services that aren't
  implemented yet in the library.

Removed
*******

- ``codingame.endpoints`` submodule.

Version 1.1.0 (2021-11-01)
--------------------------

Changed
*******

- Update `Client.login <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.login>`__ to bypass captcha on login endpoint with
  cookie based authentication, see `Login <user_guide/quickstart.html#login>`__.

Version 1.0.1 (2021-07-12)
--------------------------

Added
*****

- `CodinGamer.profile_url <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.profile_url>`__.

Version 1.0.0 (2021-07-12)
--------------------------

Added
*****

- Asynchronous client with ``Client(is_async=True)``, see `Asynchronous client <user_guide/quickstart.html#about-the-asynchronous-client>`__.

- Context managers:

    .. code-block:: python

        # synchronous
        with Client() as client:
            client.get_global_leaderboard()

        #asynchronous
        async with Client(is_async=True) as client:
            await client.get_global_leaderboard()

- More exceptions: `LoginError <https://codingame.readthedocs.io/en/stable/api.html#codingame.LoginError>`__ regroups all the exceptions related
  to login: `LoginRequired <https://codingame.readthedocs.io/en/stable/api.html#codingame.LoginRequired>`__, `EmailRequired <https://codingame.readthedocs.io/en/stable/api.html#codingame.EmailRequired>`__, `MalformedEmail <https://codingame.readthedocs.io/en/stable/api.html#codingame.MalformedEmail>`__,
  `PasswordRequired <https://codingame.readthedocs.io/en/stable/api.html#codingame.PasswordRequired>`__, `EmailNotLinked <https://codingame.readthedocs.io/en/stable/api.html#codingame.EmailNotLinked>`__ and `IncorrectPassword <https://codingame.readthedocs.io/en/stable/api.html#codingame.IncorrectPassword>`__.
  And `NotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotFound>`__ regroups `CodinGamerNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamerNotFound>`__,
  `ClashOfCodeNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.ClashOfCodeNotFound>`__, `ChallengeNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.ChallengeNotFound>`__ and `PuzzleNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.PuzzleNotFound>`__

- `ChallengeLeaderboard.has_leagues <https://codingame.readthedocs.io/en/stable/api.html#codingame.ChallengeLeaderboard.has_leagues>`__ and
  `PuzzleLeaderboard.has_leagues <https://codingame.readthedocs.io/en/stable/api.html#codingame.PuzzleLeaderboard.has_leagues>`__.

- `NotificationData._raw <https://codingame.readthedocs.io/en/stable/api.html#codingame.NotificationData._raw>`__.

Changed
*******

- Remove properties like ``CodinGamer.followers`` in favor of methods like
  `CodinGamer.get_followers <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followers>`__ to better differentiate API calls and to make
  it compatible with async API calls. Here's a list of all of the changed ones:

    - ``Client.language_ids`` -> `Client.get_language_ids <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_language_ids>`__
    - ``Client.notifications`` ->
      `Client.get_unseen_notifications <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_unseen_notifications>`__
    - ``CodinGamer.followers`` -> `CodinGamer.get_followers <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followers>`__
    - ``CodinGamer.followers_ids`` -> `CodinGamer.get_followers_ids <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followers_ids>`__
    - ``CodinGamer.following`` -> `CodinGamer.get_followed <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followed>`__
    - ``CodinGamer.following_ids`` -> `CodinGamer.get_followed_ids <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_followed_ids>`__
    - ``CodinGamer.clash_of_code_rank`` ->
      `CodinGamer.get_clash_of_code_rank <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.get_clash_of_code_rank>`__

- Make all attributes of CodinGame models read-only.

- Change type of `ClashOfCode.time_before_start <https://codingame.readthedocs.io/en/stable/api.html#codingame.ClashOfCode.time_before_start>`__ and
  `ClashOfCode.time_before_end <https://codingame.readthedocs.io/en/stable/api.html#codingame.ClashOfCode.time_before_end>`__ from `float <https://docs.python.org/library/functions.html#float>`__ to
  `datetime.timedelta <https://docs.python.org/library/datetime.html#datetime.timedelta>`__.

- Rewrite the way the client works to implement a class to manage the connection
  state and separate the `Client <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client>`__ that the user uses from the HTTP client
  that interacts with the API.

Removed
*******

- Remove argument type validation, not my fault if you can't read the docs.

Version 0.4.0 (2021-06-19)
--------------------------

Added
*****

- `Client.get_global_leaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_global_leaderboard>`__ with `GlobalLeaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.GlobalLeaderboard>`__ and
  `GlobalRankedCodinGamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.GlobalRankedCodinGamer>`__.

- `Client.get_challenge_leaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_challenge_leaderboard>`__ with
  `ChallengeLeaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.ChallengeLeaderboard>`__, `ChallengeRankedCodinGamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.ChallengeRankedCodinGamer>`__ and
  `League <https://codingame.readthedocs.io/en/stable/api.html#codingame.League>`__.

- `Client.get_puzzle_leaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_puzzle_leaderboard>`__ with `PuzzleLeaderboard <https://codingame.readthedocs.io/en/stable/api.html#codingame.PuzzleLeaderboard>`__,
  `PuzzleRankedCodinGamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.PuzzleRankedCodinGamer>`__ and `League <https://codingame.readthedocs.io/en/stable/api.html#codingame.League>`__.

Changed
*******

- Update docs style, code style and tests.

Version 0.3.5 (2020-12-10)
--------------------------

Added
*****

- Get a user with their user ID in `Client.get_codingamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_codingamer>`__.

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

- Searching for a CodinGamer with their pseudo in `Client.get_codingamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_codingamer>`__.

- `CodinGamer.xp <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer.xp>`__, thanks `@LiJu09 <https://github.com/LiJu09>`__
  (`#3 <https://github.com/takos22/codingame/pull/3>`__).

Version 0.3.2 (2020-09-23)
--------------------------

Added
*****

- `Client.get_pending_clash_of_code <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_pending_clash_of_code>`__.

Changed
*******

- Renamed ``Notification.date`` to `Notification.creation_time <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification.creation_time>`__.

Version 0.3.1 (2020-09-20)
--------------------------

Added
*****

- ``Client.notifications`` property.

- `Notification <https://codingame.readthedocs.io/en/stable/api.html#codingame.Notification>`__ class.

- `LoginRequired <https://codingame.readthedocs.io/en/stable/api.html#codingame.LoginRequired>`__ exception.

Version 0.3.0 (2020-09-20)
--------------------------

Added
*****

- `Client.login <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.login>`__.

- `Client.logged_in <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.logged_in>`__ and `Client.codingamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.codingamer>`__.

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

- `Client.get_clash_of_code <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_clash_of_code>`__.

- `ClashOfCode <https://codingame.readthedocs.io/en/stable/api.html#codingame.ClashOfCode>`__ and `Player <https://codingame.readthedocs.io/en/stable/api.html#codingame.Player>`__ classes.

- `ClashOfCodeNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.ClashOfCodeNotFound>`__ exception.

Changed
*******

- Renamed ``Client.codingamer()`` to `Client.get_codingamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client.get_codingamer>`__.

Version 0.1.0 (2020-09-12)
--------------------------

Added
*****

- `Client <https://codingame.readthedocs.io/en/stable/api.html#codingame.Client>`__ class.

- ``Client.codingamer()`` method to get a codingamer.

- `CodinGamer <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamer>`__ class.

- `CodinGamerNotFound <https://codingame.readthedocs.io/en/stable/api.html#codingame.CodinGamerNotFound>`__ exception.
