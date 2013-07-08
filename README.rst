Django MX DateTime
==================


:Author:
   Justin Quick <justquick@gmail.com>
:Version: 0.1.0
:Release: 0.1.0alpha1


Django MX DateTime uses the `mx.DateTime <http://www.egenix.com/products/python/mxBase/mxDateTime/>`_ library from `eGenix <http://www.egenix.com/>`_ to provide alternate Date, DateTime and Time fields for Django.
It works by storing the date information in the database in `Julian Day <https://en.wikipedia.org/wiki/Julian_day>`_ notation where DateFields are represented by IntegerFields and Time/DateTimeFields are represented by FloatFields.
Each field always returns an `mx.DateTime.DateTime <http://www.egenix.com/products/python/mxBase/mxDateTime/>`_ instance no matter what the internal type.

Features
--------

- Support for BCE dates
- Fuzzy parsing logic that can handle inputs like: ``Sun, 14 Jun 1998``, ``January 1 2000``, ``1.1.4004 BCE``, as well as any of the `normal Django input formats <https://docs.djangoproject.com/en/dev/ref/settings/#date-input-formats>`_.

Drawbacks
---------

- The following field lookups are not yet supported: ``year``, ``month``, ``day``, and ``week_day``
- The `admin date_hierarchy <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy>`_ setting will not work and a work-around has not yet been implemented.
- The `dates and datetimes <https://docs.djangoproject.com/en/dev/ref/models/querysets/#dates>`_ queryset methods will always return no results.
- As of now, only TimeFields and DateTimeFields have not yet been implemented. Timezones are a bitch.


Install
-------

Use pip for installation. This package requires the `egenix-mx-base <https://pypi.python.org/pypi/egenix-mx-base>`_ package which means you will need a C compiler.

::

    pip install git+https://github.com/justquick/django-mx-datetime.git#egg=django-mx-datetime

You may add ``djmx`` to your ``INSTALLED_APPS`` if you wish to test it within your project, but it is not necessary otherwise.

Compatibility
^^^^^^^^^^^^^

Django MX DateTime has been tested with all of the following setups

:Django: 1.1, 1.2, 1.3, 1.4, 1.5
:Python: 2.5, 2.6, 2.7
:Database: Sqlite3, MySQL, PostgreSQL

Usage
------

Define your models using the new fields from the djmx package:

.. code-block:: python

    from django.db import models

    from djmx.fields import DateField


    class MyModel(models.Model):
        name = models.CharField(max_length=255)
        pub_date = DateField()

        class Meta:
            ordering = ('pub_date', )

        def __unicode__(self):
            return u'%s: (published on %s)' % (self.name, self.pub_date.date)

Notice that for the unicode representation of pub_date you would use ``self.pub_date.date`` because ``self.pub_date`` will always return a ``mx.DateTime.DateTime`` which always contains time information no matter what.

Now you can setup your model in the admin:

.. code-block:: python

    from django.contrib import admin

    from djmx.admin import mx_overrides, date_format

    from .models import MyModel


    class MyModelAdmin(admin.ModelAdmin):
        formfield_overrides = mx_overrides
        list_display = ('name', 'pub_date_formatted')
        list_filter = ('-pub_date',)

        pub_date_formatted = date_format('pub_date')
        pub_date_formatted.short_description = 'Publication Date'

    admin.site.register(MyModel, MyModelAdmin)

Notice the ``mx_overrides`` dictionary which sets up the right form fields and widgets for the db fields provided by djmx.
The ``date_format`` function returns a classmethod which is used to format a date field to correctly display in the admin and retain proper ordering.

Now your model should be setup to handle all sorts of publication dates. Below is an example of command line usage:

Example
^^^^^^^

.. code-block:: python

    >>> MyModel.objects.create(name='Y2K', pub_date='January 1 2000')
    <MyModel: Y2K: (published on 2000-01-01)>
    >>> obj = MyModel.objects.get(pub_date='January 1 2000')
    >>> obj.pub_date
    <mx.DateTime.DateTime object for '2000-01-01 12:00:00.00' at 10da0bd68>
    >>> obj.pub_date.date
    '2000-01-01'
    >>> obj.pub_date.year, obj.pub_date.month, obj.pub_date.day
    (2000, 1, 1)
    >>> obj.pub_date.strftime('%A, %d. %B %Y')
    'Saturday, 01. January 2000'
    >>> obj.pub_date.pydate()  # Will not work with BCE dates
    datetime.date(2000, 1, 1)
    >>> int(obj.pub_date.jdn)  # This is what the database actually stores
    2451545

Testing
-------

The best way to test this package in all circumstances is using `Tox <http://tox.readthedocs.org/en/latest/>`_. Clone the project and run::

    $ tox

This will take a long time to download and compile all the packages required.
If you are testing database integration, make sure you have a database named "test" setup for MySQL and PostgreSQL.

You can just run the unittests at any point on the standard sqlite3 setup by running::

    $ python djmx/runtests/runtests.py

If you are using djmx in your project, you can test it like any other Django app::

    $ django-admin.py test djmx