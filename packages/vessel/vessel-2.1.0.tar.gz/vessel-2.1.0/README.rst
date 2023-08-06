Installing
==========

.. code-block:: bash

  pip3 install vessel

Cache Usage
-----------

.. code-block:: py

  import vessel

  # basic
  cache = vessel.Cache(2)
  # all methods return tuples of entries affected
  cache.create((0, 19), {'id': 0, 'age': 19, 'name': 'Hazel'} ) # hi
  cache.create((0, 23), {'id': 0, 'age': 23, 'name': 'Baiy'}  ) # hi
  cache.create((1, 21), {'id': 0, 'age': 21, 'name': 'George'}) # hi
  cache.update((0, 23), {'name': 'Bailey'}                    ) # woops
  cache.update((0,)   , {'school': '5th GL'}                  ) # new data
  cache.delete((0, 19)                                        ) # bye hazel
  cache.delete((0,)                                           ) # bye everyone

  # simple
  cache = vessel.DBCache(('id', 'age'))
  # no need to specify keys
  cache.create({'id': 0, 'age': 19, 'name': 'Hazel'} , None)
  cache.create({'id': 0, 'age': 23, 'name': 'Baiy'}  , None)
  cache.create({'id': 1, 'age': 31, 'name': 'George'}, None)
  cache.update({'id': 0, 'age': 23, 'name': 'Bailey'}, None)
  cache.update({'id': 0, 'school': '5th GL'}         , None)
  cache.delete(None                                  , (0, 19))
  cache.delete(None                                  , (0,))

Links
-----

- `Documentation <https://vessel.readthedocs.io/en/compat>`_
