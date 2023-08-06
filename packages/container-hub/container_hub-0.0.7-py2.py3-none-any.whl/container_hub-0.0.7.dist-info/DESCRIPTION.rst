=============
container-hub
=============


.. image:: https://img.shields.io/pypi/v/container-hub.svg
        :target: https://pypi.python.org/pypi/container-hub

.. image:: https://travis-ci.com/nens/container-hub.svg?token=FpwiJuZAE4pzUMeiLa1T&branch=master
        :target: https://travis-ci.com/nens/container-hub

.. image:: https://pyup.io/repos/github/nens/container-hub/shield.svg
     :target: https://pyup.io/repos/github/nens/container-hub/
     :alt: Updates


Container Hub
-------------

Spiritual successor of the machine manager. Main purpose is starting
and stopping threedi simulation containers.


Usage
-----

The container hub solely exposes two functions, ``up()`` and ``down()``. They
can be retrieved as a top level import::

    from container_hub import up
    from container_hub import down

Based on the current settings this gives you a carrier specific function,
either from the ``container_hub.carriers.marathon.container_terminal`` or the
``container_hub.carriers.docker.container_terminal``.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.0.7 (2020-02-19)
------------------

- Strip the 'simulation-' prefix when querying for the docker container_list to
  ensure uniformity between all carriers.


0.0.6 (2020-01-27)
------------------

- Use a generic `envs` arg that will set the container env variables.

- Added args `sim_uid, sim_ref_datetime, end_time, duration and start_mode` to
  container CMD.


0.0.5 (2020-01-17)
------------------

- Use generic marathon constraints settings.


0.0.4 (2019-12-19)
------------------

- Added support for host and ip lookups.


0.0.3 (2019-12-19)
------------------

- Catch also `ImportErrors` for simple settings.


0.0.2 (2019-12-19)
------------------

- Rename env var only_initialize to scheduler_action.


0.0.1 (2019-12-19)
------------------

* First release on PyPI.


