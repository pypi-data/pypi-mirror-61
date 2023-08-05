
simpy-agents
============

simpy-agents extends `SimPy <https://simpy.readthedocs.io/en/latest/>`_ by
adding the 'agent' field to events, allowing the user to track which agent is
associated with each event.

.. code-block:: python

   # Create an environment and schedule a Timeout
   env = Environment()
   env.timeout(10, agent='Test Agent')

   # The 'agent' field is passed to the event and stored in the queue
   env._queue
   >>> [(10, 1, 0, <Timeout(10) object at 0x10f913bd0>, 'Test Agent')]

   # The Environment class now has a 'scheduled_agents' property
   env.scheduled_agents
   >>> ['Test Agent']

Installation
------------

simpy-agents is installable via pip: ``pip install simpy-agents``.

All new functionality is optional and the original SimPy API is maintained. It
is recommended to remove any other installations SimPy from the environment to
ensure the intended version is imported.
