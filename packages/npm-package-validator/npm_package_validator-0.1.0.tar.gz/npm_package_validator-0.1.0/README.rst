===============================
npm-package-validator
===============================

.. image:: https://travis-ci.com/romnnn/npm_package_validator.svg?branch=master
        :target: https://travis-ci.com/romnnn/npm_package_validator
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/npm_package_validator.svg
        :target: https://pypi.python.org/pypi/npm_package_validator
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnnn/npm_package_validator
        :target: https://github.com/romnnn/npm_package_validator
        :alt: License

.. image:: https://readthedocs.org/projects/npm-package-validator/badge/?version=latest
        :target: https://npm-package-validator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/romnnn/npm_package_validator/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnnn/npm_package_validator
        :alt: Test Coverage

""""""""

Your short description here. `romnnn.github.io/npm_package_validator <https://romnnn.github.io/npm_package_validator>`_

.. code-block:: console

    $ pip install npm_package_validator

See the `official documentation`_ for more information.

.. _official documentation: https://npm-package-validator.readthedocs.io

.. code-block:: python

    import npm_package_validator

Development
-----------

For detailed instructions see `CONTRIBUTING <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
