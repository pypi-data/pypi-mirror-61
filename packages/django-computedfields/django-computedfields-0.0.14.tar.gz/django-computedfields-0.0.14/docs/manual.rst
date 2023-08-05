User Guide
==========

:mod:`django-computedfields` provides autoupdated database fields for
model methods.


Installation
------------

Install the package with pip:

.. code:: bash

    $ pip install django-computedfields

and add ``computedfields`` to your ``INSTALLED_APPS``.

For graph rendering also install :mod:`graphviz`:

.. code:: bash

    $ pip install graphviz


Settings
--------

The module respects optional settings in settings.py:

- ``COMPUTEDFIELDS_MAP``
    Used to set a file path for the pickled resolver map. To create the pickled resolver map
    point this setting to a writeable path and call the management command ``createmap``.
    This should always be used in production mode in multi process environments
    to avoid the expensive map creation on every process launch. If set, the file must
    be recreated after model changes.

- ``COMPUTEDFIELDS_ADMIN``
    Set this to ``True`` to get a listing of ``ComputedFieldsModel`` models with their field
    dependencies in admin. Useful during development.

- ``COMPUTEDFIELDS_ALLOW_RECURSION``
    Normally cycling updates to the same model field indicate an error in database design.
    Therefore the dependency resolver raises a ``CycleNodeException`` if a cycle was
    encountered. For more complicated setups (like tree structures) you can disable the
    recursion check. This comes with the drawback, that the underlying graph cannot
    linearize and optimize the update paths anymore.


Basic usage
-----------

Simply derive your model from ``ComputedFieldsModel`` and place
the ``@computed`` decorator on a method:

.. code-block:: python

    from django.db import models
    from computedfields.models import ComputedFieldsModel, computed

    class Person(ComputedFieldsModel):
        forename = models.CharField(max_length=32)
        surname = models.CharField(max_length=32)

        @computed(models.CharField(max_length=32))
        def combined(self):
            return u'%s, %s' % (self.surname, self.forename)

``combined`` will be turned into a real database field and can be accessed
and searched like any other database field. During saving the associated method gets called
and it's result written to the database. With the method ``compute('fieldname')`` you can
inspect the value that will be written, which is useful if you have pending
changes:

    >>> person = Person(forename='Leeroy', surname='Jenkins')
    >>> person.combined             # empty since not saved yet
    >>> person.compute('combined')  # outputs 'Jenkins, Leeroy'
    >>> person.save()
    >>> person.combined             # outputs 'Jenkins, Leeroy'
    >>> Person.objects.filter(combined__<some condition>)  # used in a queryset

The ``@computed`` decorator expects a model field as first argument to hold the
result of the decorated method.


Automatic Updates
-----------------

The ``@computed`` decorator understands a keyword argument ``depends`` to indicate
dependencies to related model fields. If set, the computed field gets automatically
updated upon changes of the related fields.

The example above extended by a model ``Address``:

.. code-block:: python

    class Address(ComputedFieldsModel):
        person = models.ForeignKeyField(Person)
        street = models.CharField(max_length=32)
        postal = models.CharField(max_length=32)
        city = models.CharField(max_length=32)

        @computed(models.CharField(max_length=256), depends=['person#combined'])
        def full_address(self):
            return u'%s, %s, %s %s' % (self.person.combined, self.street,
                                       self.postal, self.city)

Now if the name of a person changes, the field ``full_address`` will be updated
accordingly.

Note the format of the depends string - it consists of the relation name
and the field name separated by '#'. The field name is mandatory for any
dependency to trigger a proper update. (In fact it can be omitted for normal
fields if you never use ``.save`` with explicit setting ``update_fields``.
But that is an implementation detail you should not rely on.)
The relation name part can span serveral models, simply name the relation
in python style with a dot (e.g. ``'a.b.c'``).
A relation can be of any of foreign key, m2m, o2o and their back relations.

.. NOTE::

    The computed method gets evaluated in the model instance save method. If you
    allow relations to contain ``NULL`` values you have to handle this case explicitly:

    .. CODE:: python

        @computed(models.CharField(max_length=32), depends=['nullable_relation#field'])
        def compfield(self):
            if not self.nullable_relation:          # special handling of NULL here
                return 'something else'
            return self.nullable_relation.field     # some code referring the correct field

    Computed fields directly depending on m2m relations cannot run the associated
    method successfully on the first ``save`` if the instance was newly created
    (due to Django's order of saving the instance and m2m relations). Therefore
    you have to handle this case explicitly as well:

    .. CODE:: python

        @computed(models.CharField(max_length=32), depends=['m2m#field'])
        def compfield(self):
            if not self.pk:  # no pk yet, access to .m2m will fail
                return ''
            return ''.join(self.m2m.all().values_list('field', flat=True))

    Generally you should avoid nested m2m relations in dependendies
    as much as possible since the update penalty will explode.

.. CAUTION::

    With the depends strings you can easily end up with recursive updates.
    The dependency resolver tries to detect cycling dependencies and might
    raise a ``CycleNodeException``.

.. NOTE::

    Updates of computed fields from fields on the same model behave a little
    different than dependencies to fields on related models. To ensure proper updates,
    either call ``save`` without ``update_fields`` (full save) or
    include the computed fields explicitly in ``update_fields``:

    .. CODE:: python

        address.city = 'New City'
        address.save()                                          # also updates .full_address
        address.save(update_fields=['city'])                    # does not update .full_address
        address.save(update_fields=['city', 'full_address'])    # make it explicit

    Note that there is currently no way to circumvent this slightly different behavior
    due to the way the autoresolver works internally.
    Future versions might allow declarations like ``self#fieldname`` and handle it transparently.


Advanced Usage
--------------

For bulk creation and updates you can trigger the update of dependent computed
fields directly by calling ``update_dependent``:

    >>> from computedfields.models import update_dependent
    >>> Entry.objects.filter(pub_date__year=2010).update(comments_on=False)
    >>> update_dependent(Entry.objects.filter(pub_date__year=2010))

After multiple bulk actions consider using ``update_dependent_multi``, which
will avoid unnecessary multiplied updates.

See API Reference for further details.


Management Commands
-------------------

- ``createmap``
    recreates the pickled resolver map. Set the file path with ``COMPUTEDFIELDS_MAP``
    in settings.py.

- ``rendergraph <filename>``
    renders the dependency graph to <filename>.

- ``updatedata``
    does a full update on all computed fields in the project. Only useful after
    tons of bulk changes, e.g. from fixtures.


Todos & Future Plans
--------------------

- optimize update querysets with ``select_related`` and ``prefetch_related``


Motivation
----------

:mod:`django-computedfields` tries to be a solution to a common problem in Djangoland -
you have some neat methods on your models and want to make the results persistent
in the database for faster reads or the possibility to search over those results.
The simple approach to save the results in additional lookup fields along the model
has a big drawback - changes in related data are not reflected until the model instance
gets saved again and suddenly you find yourself in the middle of signal dispatching hell
to keep the data halfway in sync.
Suffering from this myself and inspired by odoo's computed fields I ended up writing this module.
