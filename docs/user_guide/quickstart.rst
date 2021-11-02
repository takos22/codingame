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

As of 2021-10-27, logging in with the email and the password no longer works
because of an endpoint change, see
`issue #5 <https://github.com/takos22/codingame/issues/5>`__.
The only way to fix it is to log in with cookie authentication, you need to get
the ``rememberMe`` cookie from :resource:`CodinGame <codingame>`. This cookie
should be valid for 1 year, but you might need to update it every time you log
in on CodinGame.

1. Open https://codingame.com.
2. Log into your account, if you're not logged in already.
3. Access and copy the ``rememberMe`` cookie:

    .. tab:: Chrome

        Open the developer console (:kbd:`F12`), go to the **Application** tab,
        look for the ``rememberMe`` cookie then copy its value.

        .. image:: /_static/chrome_cookie.png
           :alt: Screenshot of where to find the cookie in Chrome

    .. tab:: Firefox

        Open the developer console (:kbd:`F12`), go to the **Storage** tab,
        look for the ``rememberMe`` cookie then copy its value.

        .. image:: /_static/firefox_cookie.png
           :alt: Screenshot of where to find the cookie in Firefox

.. credits to https://github.com/s-vivien/CGBenchmark for the screenshots

4. Paste the ``rememberMe`` cookie in the code below:

.. tab::  Synchronous

    .. code-block:: python3

        import codingame

        client = codingame.Client()
        client.login(remember_me_cookie="your cookie here")

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
            await client.login(remember_me_cookie="your cookie here")

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
    Don't worry, the cookie isn't saved nor shared.

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
