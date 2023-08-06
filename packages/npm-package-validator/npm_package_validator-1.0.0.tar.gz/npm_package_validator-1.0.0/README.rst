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

.. image:: https://codecov.io/gh/romnnn/npm_package_validator/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnnn/npm_package_validator
        :alt: Test Coverage

""""""""

This python package allows you to validate nom package names.
It is a python implementation of the original `npm/validate-npm-package-name <https://github.com/npm/validate-npm-package-name>`_ written in javascript.

.. code-block:: console

    $ pip install npm_package_validator

Usage
-----

Validate an npm package name like this:

.. code-block:: python

    import npm_package_validator
    assert npm_package_validator.valid_old_package('MY-package')  # SUCCEEDS!
    assert npm_package_validator.valid_new_package('MY-package')  # FAILS! 

If you want to know whats wrong with a name, use:

.. code-block:: python

    from npm_package_validator.validate import validate_package
    errors, warnings = validate_package('MY-package')
    print("Errors: %s" % ", ".join(errors))
    print("Warnings: %s" % ", ".join(warnings))

A valid new package name must have neither ``errors`` nor ``warnings``.
Existing packages can have ``warnings``, 
as the npm validation rules have become stricter over time.

Credits
--------

This package is a port from `npm/validate-npm-package-name <https://github.com/npm/validate-npm-package-name>`_

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
