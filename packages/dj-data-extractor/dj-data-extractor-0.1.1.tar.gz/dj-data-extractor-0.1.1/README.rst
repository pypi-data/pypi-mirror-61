=============================
Data Extractor Utils
=============================

.. image:: https://badge.fury.io/py/dj-data-extractor.svg
    :target: https://badge.fury.io/py/dj-data-extractor

.. image:: https://travis-ci.org/kverdecia/dj-data-extractor.svg?branch=master
    :target: https://travis-ci.org/kverdecia/dj-data-extractor

.. image:: https://codecov.io/gh/kverdecia/dj-data-extractor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kverdecia/dj-data-extractor

Utils for extracting data from dicts.

Documentation
-------------

The full documentation is at https://dj-data-extractor.readthedocs.io.

Quickstart
----------

Install Data Extractor Utils::

    pip install dj-data-extractor

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dataextractor.apps.DataExtractorConfig',
        ...
    )

Add Data Extractor Utils's URL patterns:

.. code-block:: python

    from dataextractor import urls as dataextractor_urls


    urlpatterns = [
        ...
        url(r'^', include(dataextractor_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
