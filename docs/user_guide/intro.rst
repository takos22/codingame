.. currentmodule:: codingame

.. _intro:

Introduction
============

This is the documentation for the ``codingame`` module.

Prerequisites
-------------

**Python 3.6 or higher is required.**


.. _installing:

Installing
----------

Install ``codingame`` with pip:

.. tab:: Linux or MacOS

    .. code:: sh

        python3 -m pip install -U codingame

.. tab:: Windows

    .. code:: sh

        py -3 -m pip install -U codingame

.. _installing_async:

Installing the asynchronous version
***********************************

If you want to use the asynchronous client, make sure to have the correct
modules installed by doing:

.. tab:: Linux or MacOS

    .. code:: sh

        python3 -m pip install -U codingame[async]

.. tab:: Windows

    .. code:: sh

        py -3 -m pip install -U codingame[async]

.. _venv:

Virtual Environments
********************

Sometimes you want to keep libraries from polluting system installs or use a
different version of libraries than the ones installed on the system. You might
also not have permissions to install libraries system-wide.
For this purpose, the standard library as of Python comes with a concept
called "Virtual Environment"s to help maintain these separate versions.

A more in-depth tutorial is found on :doc:`py:tutorial/venv`.

However, for the quick and dirty:

1. Go to your project's working directory:

    .. tab:: Linux or MacOS

        .. code:: sh

            cd your-website-dir

    .. tab:: Windows

        .. code:: sh

            cd your-website-dir

2. Create a virtual environment:

    .. tab:: Linux or MacOS

        .. code:: sh

            python3 -m venv venv

    .. tab:: Windows

        .. code:: sh

            py -3 -m venv venv

3. Activate the virtual environment:

    .. tab:: Linux or MacOS

        .. code:: sh

            source venv/bin/activate

    .. tab:: Windows

        .. code:: sh

            venv\Scripts\activate.bat

4. Use pip like usual:

    .. tab:: Linux or MacOS

        .. code:: sh

            pip install -U codingame

    .. tab:: Windows

        .. code:: sh

            pip install -U codingame

Congratulations. You now have a virtual environment all set up.
You can start to code, learn more in the :doc:`quickstart`.
