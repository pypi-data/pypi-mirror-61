=============================
pyfb-reporting
=============================

.. image:: https://badge.fury.io/py/pyfb-reporting.svg
    :target: https://badge.fury.io/py/pyfb-reporting

.. image:: https://travis-ci.org/mwolff44/pyfb-reporting.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-reporting

.. image:: https://codecov.io/gh/mwolff44/pyfb-reporting/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-reporting

Your project description goes here

Documentation
-------------

The full documentation is at https://pyfb-reporting.readthedocs.io.

Quickstart
----------

Install pyfb-reporting::

    pip install pyfb-reporting

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_reporting.apps.PyfbReportingConfig',
        ...
    )

Add pyfb-reporting's URL patterns:

.. code-block:: python

    from pyfb_reporting import urls as pyfb_reporting_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_reporting_urls)),
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
