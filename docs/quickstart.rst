.. _quickstart:

.. currentmodule:: codingame

Quickstart
==========

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

Get a CodinGamer
----------------

Let's get a CodinGamer from his handle, your public handle is the 39 character length hexadecimal string at the end of your profile link.

The code will be something like this:

.. code-block:: python3

    import codingame

    client = codingame.Client()

    me = client.get_codingamer("your handle here")
    print(me)
    print(me.pseudo)
    print(me.public_handle)
    print(me.avatar_url)

Get a Clash of Code
-------------------

Let's get a Clash of Code from its handle, the public handle is the 39 character length hexadecimal string at the end of the Clash of Code invite link.

The code will be something like this:

.. code-block:: python3

    import codingame

    client = codingame.Client()

    coc = client.get_clash_of_code("clash of code handle here")
    print(coc)
    print(coc.join_url)
    print(coc.modes)
    print(coc.programming_languages)
    print(coc.public_handle)
    print(coc.players)

Login
-----

Let's log in into a profile with the email and password. There's 2 ways to log in:
1. At the :class:`Client` creation.
2. Using :meth:`Client.login`.

.. code-block:: python3

    import codingame

    client = codingame.Client()
    client.login("email", "password")
    # or
    client = codingame.Client("email", "password")

    # then you can access the logged in codingamer like this
    print(client.codingamer)
    print(client.codingamer.pseudo)
    print(client.codingamer.public_handle)
    print(client.codingamer.avatar_url)

.. note::
    Don't worry, the email and the password aren't stored.
    You can see that `here <https://github.com/takos22/codingame/blob/7cac4598f08e93b242bdf86779ef0020339d51ad/codingame/client.py#L42/>`_.
