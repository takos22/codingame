.. _quickstart:

.. currentmodule:: codingame

Quickstart
==========

This page gives a brief introduction to the module. It assumes you have the
module already installed, if you don't check the :ref:`installing` portion.
You can find examples :resource:`here <examples>`.

Get a CodinGamer
----------------

Let's get a :class:`CodinGamer` from their pseudo with the
:meth:`Client.get_codingamer` method:

.. code-block:: python3

    import codingame

    client = codingame.Client()

    codingamer = client.get_codingamer("pseudo")
    print(codingamer)
    print(codingamer.pseudo)
    print(codingamer.public_handle)
    print(codingamer.avatar_url)

.. note::
    You can also use a public handle (39 character long hexadecimal string at
    the end of its profile link) or a user ID. Just replace the ``"pseudo"``
    with the public handle or user ID.

.. seealso::
    See :meth:`Client.get_codingamer` and :class:`CodinGamer` for more info.

Get a Clash of Code
-------------------

Let's get a :class:`Clash of Code <ClashOfCode>` from its public handle with the
:meth:`Client.get_clash_of_code` method:

.. code-block:: python3

    import codingame

    client = codingame.Client()

    # get a pending public clash of code
    coc = client.get_pending_clash_of_code()
    # or get a clash of code from its public handle
    coc = client.get_clash_of_code("clash of code handle here")

    print(coc)
    print(coc.join_url)
    print(coc.modes)
    print(coc.programming_languages)
    print(coc.public_handle)
    print(coc.players)

.. note::
    The public handle is the 39 character long hexadecimal string at the end of
    the Clash of Code invite link.


.. seealso::
    See :meth:`Client.get_pending_clash_of_code`,
    :meth:`Client.get_clash_of_code` and :class:`ClashOfCode` for more info.

.. _login:

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

.. code-block:: python3

    import codingame

    client = codingame.Client(remember_me_cookie="your cookie here")

    # then you can access the logged in codingamer like this
    print(client.codingamer)
    print(client.codingamer.pseudo)
    print(client.codingamer.public_handle)
    print(client.codingamer.avatar_url)

.. seealso::
    See :class:`Client` and :meth:`Client.login` for more info.

.. note::
    Don't worry, the cookie isn't saved nor shared.
