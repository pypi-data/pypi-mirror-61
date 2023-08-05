DateStamp
===========
Automatically generates new software version stamp as ``year.month.day`` format.


Install, update & uninstall (Alpha)
-----------------------------------

Use `pip`_ to install, upgrade & uninstall:

.. code-block:: text

    pip install datestamp

    pip install --upgrade datestamp

    pip uninstall datestamp


Usage
-----

./setup.py

.. code-block:: python
    
    from datestamp import stamp

    setup(...,
          setup_requires=['datestamp'],
          version=stamp('package_name'),
          ...)


Note
----
    - New version stamp is only generated when you are ready to publish your project by
      ``python3 setup.py sdist`` or current version date is used.
    - When new date is generated at ``setup(version=stamp(...))`` it also replaces ``__version__`` line with ``__version__ = '2020.2.9'`` in ``__init__.py`` file.
    - Works for One-Off script file as well like ``datestamp`` package itself.


License
-------
Free, No limit what so ever. `Read more`_


.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _Read more: https://github.com/YoSTEALTH/datestamp/blob/master/LICENSE.txt
