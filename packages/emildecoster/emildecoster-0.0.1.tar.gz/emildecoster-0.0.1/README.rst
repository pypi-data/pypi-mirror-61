========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-emildecoster/badge/?style=flat
    :target: https://readthedocs.org/projects/python-emildecoster
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/Emil-Decoster/python-emildecoster.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Emil-Decoster/python-emildecoster

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Emil-Decoster/python-emildecoster?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/Emil-Decoster/python-emildecoster

.. |requires| image:: https://requires.io/github/Emil-Decoster/python-emildecoster/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Emil-Decoster/python-emildecoster/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/Emil-Decoster/python-emildecoster/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Emil-Decoster/python-emildecoster

.. |version| image:: https://img.shields.io/pypi/v/emildecoster.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/emildecoster

.. |wheel| image:: https://img.shields.io/pypi/wheel/emildecoster.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/emildecoster

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/emildecoster.svg
    :alt: Supported versions
    :target: https://pypi.org/project/emildecoster

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/emildecoster.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/emildecoster

.. |commits-since| image:: https://img.shields.io/github/commits-since/Emil-Decoster/python-emildecoster/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/Emil-Decoster/python-emildecoster/compare/v0.0.1...master



.. end-badges

This is my first test-package.

Installation
============

::

    pip install emildecoster

You can also install the in-development version with::

    pip install https://github.com/Emil-Decoster/python-emildecoster/archive/master.zip


Documentation
=============


https://python-emildecoster.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
