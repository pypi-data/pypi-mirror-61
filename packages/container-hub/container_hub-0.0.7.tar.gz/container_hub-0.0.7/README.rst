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
