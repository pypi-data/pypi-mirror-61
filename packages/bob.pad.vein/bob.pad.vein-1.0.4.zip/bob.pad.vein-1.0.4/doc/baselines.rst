.. vim: set fileencoding=utf-8 :
.. date: Thu Sep 20 11:58:57 CEST 2012

.. _bob.pad.vein.baselines:

===============================
 Executing Baseline Algorithms
===============================

The first thing you might want to do is to execute one of the vein presentation
attack detection algorithms that are implemented in ``bob.pad.vein``.


Running Baseline Experiments
----------------------------

Currently, there is only one available baseline in this package, based on the
work from [TREA15]_, using Fourier Transforms. You can run this baseline and
draw comparisons to other results presented on the *1st Competition on Counter
Measures to Finger Vein Spoofing Attacks* since scores from the competition are
included in this package for reproducibility purposes.

To run the baseline experiments, you can use the ``spoof.py`` script by just
going to the console and typing:

.. code-block:: sh

   $ spoof.py


This script is explained in more detail in :ref:`bob.pad.base.experiments`.
The ``spoof.py --help`` option shows you, which other options you can set.

Usually it is a good idea to have at least verbose level 2 (i.e., calling
``spoof.py --verbose --verbose``, or the short version ``spoof.py
-vv``).

.. note:: **Running in Parallel**

   To run the experiments in parallel, you can define an SGE grid or local host
   (multi-processing) configurations as explained in
   :ref:`running_in_parallel`.

   In short, to run in the Idiap SGE grid, you can simply add the ``--grid``

   command line option, without parameters. To run experiments in parallel on
   the local machine, simply add a ``--parallel <N>`` option, where ``<N>``
   specifies the number of parallel jobs you want to execute.


Database setups and baselines are encoded using
:ref:`bob.bio.base.configuration-files`, all stored inside the package root, in
the directory ``bob/pad/vein/configurations``. Documentation for each resource
is available on the section :ref:`bob.pad.vein.resources`.

.. warning::

   You **cannot** run experiments just by executing the command line
   instructions described in this guide. You **need first** to procure yourself
   the raw data files that correspond to *each* database used here in order to
   correctly run experiments with those data. Biometric data is considered
   private data and, under EU regulations, cannot be distributed without a
   consent or license. You may consult our
   :ref:`bob.pad.vein.resources.databases` resources section for checking
   currently supported databases and accessing download links for the raw data
   files.

   Once the raw data files have been downloaded, particular attention should be
   given to the directory locations of those. Unpack the databases carefully
   and annotate the root directory where they have been unpacked.

   Then, carefully read the *Databases* section of
   :ref:`bob.bio.base.installation` on how to correctly setup the
   ``~/.bob_bio_databases.txt`` file.

   Use the following keywords on the left side of the assignment (see
   :ref:`bob.pad.vein.resources.databases`):

   .. code-block:: text

      [YOUR_VERAFINGER_DIRECTORY] = /complete/path/to/verafinger

   Notice it is rather important to use the strings as described above,
   otherwise ``bob.pad.base`` will not be able to correctly load your images.

   Once this step is done, you can proceed with the instructions below.


In the remainder of this section we introduce baseline experiments you can
readily run with this tool without further configuration. The only baseline
examplified in this guide was published in [TREA15]_.


PAD using Fast-Fourier Transform based Features
===============================================

Detailed description at :ref:`bob.pad.vein.resources.detection.fourier`.

To run the baseline on the `VERA fingervein`_ database, using the ``full``
protocol, do the following:


.. code-block:: sh

   $ spoof.py verafinger-pad fourier -vv


.. tip::

   If you have more processing cores on your local machine and don't want to
   submit your job for SGE execution, you can run it in parallel (using 4
   parallel tasks) by adding the options ``--parallel=4 --nice=10``. **Before**
   doing so, make sure the package gridtk_ is properly installed.

   Optionally, you may use the ``parallel`` resource configuration which
   already sets the number of parallel jobs to the number of hardware cores you
   have installed on your machine (as with
   :py:func:`multiprocessing.cpu_count`) and sets ``nice=10``. For example:

   .. code-block:: sh

      $ spoof.py verafinger-pad fourier parallel -vv

   To run on the Idiap SGE grid using our stock
   io-big-48-slots-4G-memory-enabled (see
   :py:mod:`bob.pad.vein.configurations.gridio4g48`) configuration, use:

   .. code-block:: sh

      $ spoof.py verafinger-pad fourier grid -vv

   You may also, optionally, use the configuration resource ``gridio4g48``,
   which is just an alias of ``grid`` in this package.



This command line selects and runs the following implementations for the
toolchain:

* :ref:`bob.pad.vein.resources.database.verafinger`
* :ref:`bob.pad.vein.resources.detection.fourier`

As the tool runs, you'll see printouts that show how it advances through
preprocessing, feature extraction and presentation attack detection.

To complete the evaluation, run the command bellow, that will output the equal
error rate (EER) and plot the detector error trade-off (DET) curve with the
performance:

.. code-block:: sh

   $ bob_compute_perf.py --no-plot <path-to>/results/fourier/full/nonorm/scores-{dev,eval}
   [Min. criterion: EER] Threshold on Development set: 5.340000e-01
          | Development    | Test
   -------+----------------+-----------------
     FMR  | 0.000% (0/120) | 0.000% (0/200)
     FNMR | 0.000% (0/120) | 0.000% (0/200)
     HTER | 0.000%         | 0.000%


If you do the same analysis for the ``cropped`` protocol, you should observe
the following output:


.. code-block:: sh

   $ bob_compute_perf.py --no-plot <path-to>/results/fourier/cropped/nonorm/scores-{dev,eval}
   [Min. criterion: EER] Threshold on Development set: 5.766667e-01
          | Development      | Test
   -------+------------------+-------------------
     FMR  | 24.167% (29/120) | 21.500% (43/200)
     FNMR | 24.167% (29/120) | 16.500% (33/200)
     HTER | 24.167%          | 19.000%


Modifying Baseline Experiments
------------------------------

It is fairly easy to modify baseline experiments available in this package. To
do so, you must copy the configuration files for the given baseline you want to
modify, edit them to make the desired changes and run the experiment again.

For example, suppose you'd like to change the protocol on the Vera Fingervein
database and use the protocol ``cropped`` instead of the default protocol
``full``.  First, you identify where the configuration file sits:

.. code-block:: sh

   $ resources.py -tc -p bob.pad.vein
   - bob.pad.vein X.Y.Z @ /path/to/bob.pad.vein:
     + verafinger-pad --> bob.pad.vein.configurations.verafinger
     + fourier        --> bob.pad.vein.configurations.fourier


The listing above tells the ``verafinger`` configuration file sits on the
file ``/path/to/bob.pad.vein/bob/pad/vein/configurations/verafinger.py``. In
order to modify it, make a local copy. For example:

.. code-block:: sh

   $ cp /path/to/bob.pad.vein/bob/pad/vein/configurations/verafinger.py verafinger_cropped.py
   $ # edit verafinger_cropped.py, change the value of "protocol" to "cropped"


Also, don't forget to change all relative module imports (such as ``from
..database.verafinger import Database``) to absolute imports (e.g. ``from
bob.pad.vein.database.verafinger import Database``). This will make the
configuration file work irrespectively of its location w.r.t. ``bob.pad.vein``.
The final version of the modified file could look like this:

.. code-block:: python

   from bob.pad.vein.database.verafinger import Database

   database = Database(original_directory='/where/you/have/the/raw/files',
     original_extension='.png', #don't change this
     )

   protocol = 'cropped'


Now, re-run the experiment using your modified database descriptor:

.. code-block:: sh

   $ spoof.py ./verafinger_cropped.py fourier -vv


Notice we replace the use of the registered configuration file named
``verafinger-pad`` by the local file ``verafinger_cropped.py``. This makes the
program ``spoof.py`` take that into consideration instead of the original file.


.. include:: links.rst
