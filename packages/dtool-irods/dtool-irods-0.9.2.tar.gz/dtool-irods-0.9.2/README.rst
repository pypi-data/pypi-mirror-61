Add iRODS support to dtool
==========================

.. image:: https://badge.fury.io/py/dtool-irods.svg
   :target: http://badge.fury.io/py/dtool-irods
   :alt: PyPi package

- GitHub: https://github.com/jic-dtool/dtool-irods
- PyPI: https://pypi.python.org/pypi/dtool-irods
- Free software: MIT License


Features
--------

- Copy datasets to and from iRODS
- List all the datasets in an iRODS zone
- Create datasets directly in iRODS

Installation
------------

To install the dtool-irods package.

.. code-block:: bash

    pip install dtool-irods


Usage
-----

To copy a dataset from local disk (``my-dataset``) to an iRODS zone
(``/data_raw``) one can use the command below.

.. code-block::

    dtool copy ./my-dataset /data_raw irods

To list all the datasets in an iRODS zone one can use the command below.

.. code-block::

    dtool ls /data_raw irods

See the `dtool documentation <http://dtool.readthedocs.io>`_ for more detail.


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-symlink <https://github.com/jic-dtool/dtool-symlink>`_
