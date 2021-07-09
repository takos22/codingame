.. _async:

.. currentmodule:: codingame

Asynchronous client
===================

The :class:`asynchronous client <~codingame.client.async_.AsyncClient>` has the
same methods as the :class:`synchronous client <~codingame.client.sync.SyncClient>`,
but all of them are `coroutines <coroutine_link>`_. That means that you can use
methods like :meth:`Client.login`, but you need to do ``await client.login(...)``
instead of ``client.login(...)``.

It works like this for methods of CodinGame models like :meth:`CodinGamer.get_followers`
needs to be awaited with the asynchronous client.

Example
-------

Here's the first block of code of :ref:`quickstart` but with the asynchronous client:

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
