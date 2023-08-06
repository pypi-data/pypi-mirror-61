.. vim: set fileencoding=utf-8 :
.. Mon 11 Jul 2016 16:39:15 CEST


.. _bob.pad.vein.resources:

===========
 Resources
===========

This section contains a listing of all ready-to-use resources you can find in
this package. Each module may contain references different resource types,
including ``database``, ``preprocessor``, ``extractor`` and ``algorithm``. By
combining *complementary* resources, you can run baseline experiments as
explained on :ref:`bob.pad.vein.baselines`.


.. _bob.pad.vein.resources.databases:

Databases
---------

These resources represent configuration files containing at least settings for
the following runtime attributes of ``spoof.py``:

  * ``database``
  * ``protocol``


.. _bob.pad.vein.resources.database.verafinger:

Verafinger Database
===================

.. automodule:: bob.pad.vein.configurations.verafinger
   :members:


.. _bob.pad.vein.resources.detection:

PA Detection Systems
--------------------

These resources represent configuration files containing at least settings for
the following runtime attributes of ``spoof.py``:

  * ``sub_directory``
  * ``preprocessor``
  * ``extractor``
  * ``algorithm``


.. _bob.pad.vein.resources.detection.fourier:

Fast Fourier Transform-based Features
=====================================

.. automodule:: bob.pad.vein.configurations.fourier
   :members:


Other Resources
---------------

Other resources which include configuration parameters for circumstantial
usage.

.. _bob.pad.vein.resources.parallel:


Parallel Running
================

.. automodule:: bob.pad.vein.configurations.parallel
   :members:


Using SGE at Idiap
==================

.. automodule:: bob.pad.vein.configurations.gridio4g48
   :members:

.. include:: links.rst
