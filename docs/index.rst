dotenvfile -- a .env file Parser for Python
===========================================

Installing
----------

Find `dotenvfile on PyPI`_.  Install it using pip_::

   $ pip install dotenvfile

.. _`dotenvfile on PyPI`: https://pypi.python.org/pypi/dotenvfile
.. _pip: https://pip.readthedocs.org/

Contributing
------------

Contributions welcome!  Fork `dotenvfile on GitHub`_ and send in a pull
request!

.. _`dotenvfile on GitHub`: https://github.com/smartmob-project/dotenvfile

Getting started
---------------

.. testcode::

   import json
   import dotenvfile
   process_types = dotenvfile.loads('''
   REDIS_URL=redis+tcp://localhost:6379/0
   ''')
   print(json.dumps(process_types, indent=2, sort_keys=True))

.. testoutput::

   {
     "REDIS_URL": "redis+tcp://localhost:6379/0"
   }

API reference
-------------

.. automodule:: dotenvfile

   .. autofunction:: loads
   .. autofunction:: load
   .. autofunction:: loadfile

