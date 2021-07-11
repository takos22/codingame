.. currentmodule:: codingame

Changelog
=========

v1.0.0
------

Rewrite.

- Add support for asynchronous client with ``Client(is_async=True)``, see
  :ref:`async`.

- Add support for context managers:

    .. code-block:: python

        # synchronous
        with Client() as client:
            client.get_global_leaderboard()

        #asynchronous
        async with Client(is_async=True) as client:
            await client.get_global_leaderboard()


- Remove properties like ``CodinGamer.followers`` in favor of methods like
  :meth:`CodinGamer.get_followers` to better differentiate API calls and to make
  it compatible with async API calls. Here's a list of all of the changed ones:

    - :attr:`Client.language_ids` -> :meth:`Client.get_language_ids`
    - :attr:`Client.unseen_notifications` ->
      :meth:`Client.get_unseen_notifications`
    - :attr:`CodinGamer.followers` -> :meth:`CodinGamer.get_followers`
    - :attr:`CodinGamer.followers_ids` -> :meth:`CodinGamer.get_followers_ids`
    - :attr:`CodinGamer.following` -> :meth:`CodinGamer.get_followed`
    - :attr:`CodinGamer.following_ids` -> :meth:`CodinGamer.get_followed_ids`
    - :attr:`CodinGamer.clash_of_code_rank` ->
      :meth:`CodinGamer.get_clash_of_code_rank`

- Add more exceptions: :exc:`LoginError` regroups all the exceptions related
  to login: :exc:`LoginRequired`, :exc:`EmailRequired`, :exc:`MalformedEmail`,
  :exc:`PasswordRequired`, :exc:`EmailNotLinked` and :exc:`IncorrectPassword`.
  And :exc:`NotFound` regroups :exc:`CodinGamerNotFound`,
  :exc:`ClashOfCodeNotFound`, :exc:`ChallengeNotFound` and :exc:`PuzzleNotFound`

- Make all attributes of CodinGame models read-only.

- Add :attr:`ChallengeLeaderboard.has_leagues` and
  :attr:`PuzzleLeaderboard.has_leagues`.

- Add :attr:`Notification._raw`.

- Change :attr:`ClashOfCode.time_before_start` and
  :attr:`ClashOfCode.time_before_end` from :class:`float` to
  :class:`datetime.timedelta`.

- Remove argument type validation, not my fault if you can't read the docs.

- Rewrite the way the client works to implement a class to manage the connection
  state and separate the :class:`Client` that the user uses from the HTTP client
  that interacts with the API.

v0.4.0
------

Leaderboards support.

- Add :meth:`Client.get_global_leaderboard` with :class:`GlobalLeaderboard` and
  :class:`GlobalRankedCodinGamer`.

- Add :meth:`Client.get_challenge_leaderboard` with
  :class:`ChallengeLeaderboard`, :class:`ChallengeRankedCodinGamer` and
  :class:`League`.

- Add :meth:`Client.get_puzzle_leaderboard` with :class:`PuzzleLeaderboard`,
  :class:`PuzzleRankedCodinGamer` and :class:`League`.

- Update docs style, code style and tests.

v0.3.5
------

- Add support for user IDs in :meth:`Client.get_codingamer`.

- Add :attr:`CodinGamer.followers_ids` and :attr:`CodinGamer.following_ids` to
  get information about followed users and followers without logging in.

- Add :attr:`CodinGamer.clash_of_code_rank`.

v0.3.4
------

- Add support for python 3.9.

v0.3.3
------

- Add support for usernames in :meth:`Client.get_codingamer`.

- Add :attr:`CodinGamer.xp`.

v0.3.2
------

Pending Clash of Code support.

- Add :meth:`Client.get_pending_clash_of_code`.

- Change :attr:`Notification.date` to :attr:`Notification.creation_time`.

v0.3.1
------

Notification support.

- Add :attr:`Client.notifications` property and :class:`Notification` class.

- Add :exc:`LoginRequired` exception.

v0.3.0
------

Login support.

- Add :meth:`Client.login`.

- Add :attr:`Client.logged_in` and :attr:`Client.codingamer`.

- Add :attr:`Client.language_ids` property.

- Add :attr:`CodinGamer.followers` and :attr:`CodinGamer.following` properties.

v0.2.1
------

- Add argument type validation.

v0.2.0
------

Clash of Code support.

- Add :meth:`Client.get_clash_of_code`, :class:`ClashOfCode`, :class:`Player`
  and :exc:`ClashOfCodeNotFound`.

- Change ``Client.codingamer()`` to :meth:`Client.get_codingamer`.

v0.1.0
------

First release.

- Add :class:`Client`.

- Add ``Client.codingamer()``, :class:`CodinGamer` and
  :exc:`CodinGamerNotFound`.
