=====
Usage
=====

To use shade in a project:

.. code-block:: python

  import shade

For a simple example, see :ref:`usage_example`.

.. note::
  API methods that return a description of an OpenStack resource (e.g.,
  server instance, image, volume, etc.) do so using a `munch.Munch` object
  from the `Munch library <https://github.com/Infinidat/munch>`_. `Munch`
  objects can be accessed using either dictionary or object notation
  (e.g., ``server.id``, ``image.name`` and ``server['id']``, ``image['name']``)

.. autoclass:: shade.OpenStackCloud
   :members:
