=================================
Django flexible filter conditions
=================================

.. image:: https://badge.fury.io/py/django-flexible-filter-conditions.svg
    :target: https://badge.fury.io/py/django-flexible-filter-conditions

.. image:: https://travis-ci.org/PetrDlouhy/django-flexible-filter-conditions.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/django-flexible-filter-conditions

.. image:: https://codecov.io/gh/PetrDlouhy/django-flexible-filter-conditions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/django-flexible-filter-conditions

Flexible query filter conditions, that can be defined from django-admin and used for segmentation of date (i.e. Profiles).

Documentation
-------------

The full documentation is at https://django-flexible-filter-conditions.readthedocs.io.

Quickstart
----------

Install Django flexible filter conditions::

    pip install django-flexible-filter_conditions

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'flexible_filter_conditions.apps.FlexibleFilterConditionsConfig',
        ...
    )

Add Django flexible filter conditions's URL patterns:

.. code-block:: python

    FLEXIBLE_FILTER_CONDITIONS_FIELD_MAP = {
        'User': ('aklub.models', 'User'),
        'Profile': ('aklub.models', 'Profile'),
        'Payment': ('aklub.models', 'Payment'),
        'User.last_payment': ('aklub.models', 'Payment'),
        'User.userchannels': ('aklub.models', 'DonorPaymentChannel'),
    }



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
