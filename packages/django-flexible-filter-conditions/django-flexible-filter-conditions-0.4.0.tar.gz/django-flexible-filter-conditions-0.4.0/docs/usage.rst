=====
Usage
=====

To use Django flexible filter conditions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'flexible_filter_conditions.apps.FlexibleFilterConditionsConfig',
        ...
    )

Configure fields that you want to filter on in your settings:

.. code-block:: python

  FLEXIBLE_FILTER_CONDITIONS_FIELD_MAP = {
      'User': ('aklub.models', 'User'),
      'Profile': ('aklub.models', 'Profile'),
      'Payment': ('aklub.models', 'Payment'),
      'User.last_payment': ('aklub.models', 'Payment'),
      'User.userchannels': ('aklub.models', 'DonorPaymentChannel'),
  }

