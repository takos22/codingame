.. _quickstart:

.. currentmodule:: codingame

Quickstart
==========

This page gives a brief introduction to the module. It assumes you have the
module already installed, if you don't check the :ref:`installing` portion.
You can find examples :resource:`here <examples>`.

You can switch between the tutorial for the synchronous client and the
asynchronous client with the tabs.

.. _async:

About the asynchronous client
-----------------------------

.. note::
    If you're new to Python or you don't need to use the asynchronous client,
    you can probably skip this section.

The :class:`asynchronous client <codingame.client.async_.AsyncClient>`
has the same methods as the
:class:`synchronous client <codingame.client.sync.SyncClient>`, but all of
them are `coroutines <coroutine_link>`_. That means that you can use methods
like :meth:`Client.login`, but you need to do ``await client.login(...)``
instead of ``client.login(...)``.

It works like this for methods of CodinGame models, like
:meth:`CodinGamer.get_followers` needs to be awaited with the asynchronous
client.

Get a CodinGamer
----------------

Getting a :class:`CodinGamer` from their pseudo with the
:meth:`Client.get_codingamer` method:

.. tab::  Synchronous

    .. code-block:: python3

        import codingame

        client = codingame.Client()

        codingamer = client.get_codingamer("pseudo")
        print(codingamer)
        print(codingamer.pseudo)
        print(codingamer.public_handle)
        print(codingamer.avatar_url)

.. tab::  Asynchronous

    .. code-block:: python3

        import codingame
        import asyncio

        async def main():
            client = codingame.Client(is_async=True)

            codingamer = await client.get_codingamer("pseudo")
            print(codingamer)
            print(codingamer.pseudo)
            print(codingamer.public_handle)
            print(codingamer.avatar_url)

        asyncio.run(main())

.. note::
    You can also use a public handle (39 character long hexadecimal string at
    the end of its profile link) or a user ID. Just replace the ``"pseudo"``
    with the public handle or user ID.

.. seealso::
    See :meth:`Client.get_codingamer` and :class:`CodinGamer` for more info.

Get a Clash of Code
-------------------

Getting a :class:`Clash of Code <ClashOfCode>` from its public handle with the
:meth:`Client.get_clash_of_code` method or the next public clash with
:meth:`Client.get_pending_clash_of_code`:

.. tab::  Synchronous

    .. code-block:: python3

        import codingame

        client = codingame.Client()

        # get a clash of code from its handle
        coc = client.get_clash_of_code("handle")
        # or get the next public clash
        coc = client.get_pending_clash_of_code()

        print(coc)
        print(coc.join_url)
        print(coc.modes)
        print(coc.programming_languages)
        print(coc.public_handle)
        print(coc.players)

.. tab::  Asynchronous

    .. code-block:: python3

        import codingame
        import asyncio

        async def main():
            client = codingame.Client(is_async=True)

            # get a clash of code from its handle
            coc = await client.get_clash_of_code("handle")
            # or get the next public clash
            coc = await client.get_pending_clash_of_code()

            print(coc)
            print(coc.join_url)
            print(coc.modes)
            print(coc.programming_languages)
            print(coc.public_handle)
            print(coc.players)

        asyncio.run(main())

.. note::
    The public handle is the 39 character long hexadecimal string at the end of
    the Clash of Code invite link.


.. seealso::
    See :meth:`Client.get_clash_of_code`,
    :meth:`Client.get_pending_clash_of_code` and :class:`ClashOfCode`
    for more info.

Login
-----

Logging in into a CodinGame account with the email and password with the
:meth:`Client.login` method:

.. tab::  Synchronous

    .. code-block:: python3

        import codingame

        client = codingame.Client()
        client.login("email", "password")

        # then you can access the logged in codingamer like this
        print(client.logged_in)
        print(client.codingamer)
        print(client.codingamer.pseudo)
        print(client.codingamer.public_handle)
        print(client.codingamer.avatar_url)

.. tab::  Asynchronous

    .. code-block:: python3

        import codingame
        import asyncio

        async def main():
            client = codingame.Client(is_async=True)
            await client.login("email", "password")

            # then you can access the logged in codingamer like this
            print(client.logged_in)
            print(client.codingamer)
            print(client.codingamer.pseudo)
            print(client.codingamer.public_handle)
            print(client.codingamer.avatar_url)

        asyncio.run(main())

.. seealso::
    See :class:`Client` and :meth:`Client.login` for more info.

.. note::
    Don't worry, the email and the password aren't stored.
    You can see that `here <https://github.com/takos22/codingame/blob/master/codingame/client/sync.py#L23-33/>`__.

Once you are logged in, you have access to many more methods of the
:class:`Client`, like :meth:`Client.get_unseen_notifications`, and of the logged
in :class:`CodinGamer`, like :meth:`CodinGamer.get_followers`.

Get unseen notifications
------------------------

Getting a :class:`list` of the unseen :class:`notifications <Notification>` of
the logged in :class:`CodinGamer` with the
:meth:`Client.get_unseen_notifications` method:

.. tab::  Synchronous

    .. code-block:: python3

        import codingame

        client = codingame.Client()
        client.login("email", "password")

        notifications = client.get_unseen_notifications()

        print(f"{len(notifications)} unseen notifications:")
        for notification in notifications:
            print(notification.type_group, notification.type)

.. tab::  Asynchronous

    .. code-block:: python3

        import codingame
        import asyncio

        async def main():
            client = codingame.Client(is_async=True)
            await client.login("email", "password")

            notifications = await client.get_unseen_notifications()

            print(f"{len(notifications)} unseen notifications:")
            for notification in notifications:
                print(notification.type_group, notification.type)

        asyncio.run(main())

.. seealso::
    See :meth:`Client.get_unseen_notifications` and :class:`Notification` for
    more info.
