.. _quickstart:

.. currentmodule:: codingame

Quickstart
==========

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

A Minimal Client
----------------

Let's get a CodinGamer from his handle, your public handle is the 39 character length hexadecimal string at the end of your profile link.

It looks something like this:

.. code-block:: python3

    import codingame

    client = codingame.Client()

    me = client.codingamer("your handle here")
    print(me)
    print(me.pseudo)
    print(me.public_handle)
    print(me.avatar_url)

Let's name this file ``example_codingame.py``. Make sure not to name it ``codingame.py`` as that'll conflict
with the library.
