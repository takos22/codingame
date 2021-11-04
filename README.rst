codingame API wrapper
=====================

.. image:: https://img.shields.io/pypi/v/codingame?color=blue
    :target: https://pypi.python.org/pypi/codingame
    :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/codingame?color=orange
    :target: https://pypi.python.org/pypi/codingame
    :alt: Supported Python versions
.. image:: https://img.shields.io/github/checks-status/takos22/codingame/master?label=tests
    :target: https://github.com/takos22/codingame/actions/workflows/lint-test.yml
    :alt: Lint and test workflow status
.. image:: https://readthedocs.org/projects/codingame/badge/?version=latest
    :target: https://codingame.readthedocs.io
    :alt: Documentation build status
.. image:: https://codecov.io/gh/takos22/codingame/branch/master/graph/badge.svg?token=HQ3J3034Y2
    :target: https://codecov.io/gh/takos22/codingame
    :alt: Code coverage
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: Black
.. image:: https://img.shields.io/discord/754028526079836251.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
    :target: https://discord.gg/8HgtN6E
    :alt: Discord support server

Pythonic wrapper for the undocumented `CodinGame <https://www.codingame.com/>`_ API.


Installation
------------

**Python 3.6 or higher is required.**

Install ``codingame`` with pip:

.. code:: sh

   pip install codingame


Quickstart
----------

Create an application, in ``example.py``:

.. code:: python

   import codingame

   client = codingame.Client()

   # get a codingamer
   codingamer = client.get_codingamer("username")
   print(codingamer.pseudo)

   # get the global leaderboard
   global_leaderboard = client.get_global_leaderboard()
   # print the pseudo of the top codingamer
   print(global_leaderboard.users[0].pseudo)

See `the docs <https://codingame.readthedocs.io/en/stable/user_guide/quickstart.html>`__.

Contribute
----------

- `Source Code <https://github.com/takos22/codingame>`_
- `Issue Tracker <https://github.com/takos22/codingame/issues>`_


Support
-------

If you are having issues, please let me know by joining the discord support server at https://discord.gg/8HgtN6E

License
-------

The project is licensed under the MIT license.

Links
------

- `PyPi <https://pypi.org/project/codingame/>`_
- `Documentation <https://codingame.readthedocs.io/en/latest/index.html>`_
- `Discord support server <https://discord.gg/8HgtN6E>`_
