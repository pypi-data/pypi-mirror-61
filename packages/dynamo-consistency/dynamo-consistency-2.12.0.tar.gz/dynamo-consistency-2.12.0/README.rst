.. _intro-ref:

Introduction
============

|build-status|

Dynamo Consistency is the consistency plugin for Dynamo Dynamic Data Management System.
Even though Dynamo controls and tracks the history of file transfers between computing sites,
a separate check is needed to ensure files are not lost or accumulated during user or system errors.
Sites that can no longer access files after a power outage, for example,
can cause other problems for the entire data management system.
Transfers requested from the site to another site will fail for missing files.
Sites are chosen incorrectly for production jobs that assume the presence of a local file.
Last disk copies may also be missing, causing a delay for user requests for data.
Another type of inconsistency is caused when files thought to be deleted are still on disk.
This leads to wasted disk space for files that are not accessed, except by accident.
Dynamo Consistency does its check by regularly listing each remote site and
comparing the listed contents to Dynamo's inventory database.

Some executables, described in :ref:`execute-ref`, are provided to run the check.
The package also includes a number of modules that can be imported independently
to create custom consistency check runs.
These are described more in :ref:`frontend-ref`.
A simple consistency check on a site can be done by doing the following
when an instance of ``dynamo`` is installed::

  from dynamo_consistency import config, datatypes, remotelister, inventorylister

  config.LOCATION = '/path/to/config.json'
  site = 'T2_US_MIT'                        # For example

  inventory_listing = inventorylister.listing(site)
  remote_listing = remotelister.listing(site)

  datatypes.compare(inventory_listing, remote_listing, 'results')

In this example,
the list of file LFNs in the inventory and not at the site will be in ``results_missing.txt``.
The list of file LFNs at the site and not in the inventory will be in ``results_orphan.txt``.
The ``listing`` functions can be re-implemented to perform the check desired.
This is detailed more in :ref:`backend-ref`.

Installation
++++++++++++

Dynamo Consistency requires the `XRootD <http://xrootd.org/doc/python/xrootd-python-0.1.0/>`_ Python module to be installed separately.
In addition, it uses the Dynamo Dynamic Data Management package to get inventory listings
and to report results of the consistency check.
Any other needed packages are installed with Dynamo Consistency during installation.

The simplest way to install is through pip::

  pip install dynamo-consistency

The source code is maintained on `GitHub <https://github.com/SmartDataProjects/dynamo-consistency>`_.
Other typical ``setuptools`` methods are supported by the repository's ``setup.py``.

.. |build-status| image:: https://travis-ci.org/SmartDataProjects/dynamo-consistency.svg?branch=master
   :target: https://travis-ci.org/SmartDataProjects/dynamo-consistency
