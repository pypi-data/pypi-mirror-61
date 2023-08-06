.. vim: set fileencoding=utf-8 :

.. _bob.pad.vein:

======================================================
 Library for Vein Presentation Attack Detection (PAD)
======================================================

This library is an open source tool consisting of a series of plugins for
bob.pad.base_, our open-source presentation-attack detection platform. As a
result, it is fully extensible using bob.pad.base_ documented types and
techniques. Please refer to the manual of that package for a thorough
introduction. In this guide, we focus on details concerning vein PAD
experiments using our plugins.

If you use this package in your publication, please cite the following paper
on your references:

.. code-block:: bibtex

  @inproceedings{Tome_ICB2015_AntiSpoofFVCompetition,
    author = {Tome, Pedro and Raghavendra, R. and Busch, Christoph and Tirunagari, Santosh and Poh, Norman and Shekar, B. H. and Gragnaniello, Diego and Sansone, Carlo and Verdoliva, Luisa and Marcel, S{\'{e}}bastien},
    keywords = {Biometrics, Finger vein, Spoofing Attacks, Anti-spoofing},
    month = may,
    title = {The 1st Competition on Counter Measures to Finger Vein Spoofing Attacks},
    booktitle = {The 8th IAPR International Conference on Biometrics (ICB)},
    year = {2015},
    location = {Phuket, Thailand},
    url = {http://publications.idiap.ch/index.php/publications/show/3095}
  }


Users Guide
===========

.. toctree::
   :maxdepth: 2

   baselines
   references
   resources
   api

.. todolist::

.. include:: links.rst
