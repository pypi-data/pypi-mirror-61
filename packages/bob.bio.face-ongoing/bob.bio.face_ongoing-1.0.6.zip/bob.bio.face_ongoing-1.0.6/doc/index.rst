.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

.. _bob.bio.face_ongoing:

=========================
 Face Recognition OnGoing
=========================

The goal of this package is to provide an "easy to reproduce" set of experiments in some large scale
face recognition databases.
This package is an extension of the `bob.bio.base <https://www.idiap.ch/software/bob/docs/bob/bob.bio.base/stable/index.html>`_ framework.


Installation
============

The installation instructions are based on conda (**LINUX ONLY**).
Please `install conda <https://conda.io/docs/install/quick.html#linux-miniconda-install>`_ before continuing.


After everything installed do::

  $ conda install bob.bio.face_ongoing
  $ bob bio face_ongoing download_models <DESTINATION_PATH>


If you want to developt this package do ::

  $ git clone https://gitlab.idiap.ch/bob/bob.bio.face_ongoing
  $ cd bob.bio.face_ongoing
  $ conda env create -f environment.yml
  $ source activate bob.bio.face_ongoing  # activate the environment
  $ buildout

This software component contains all the necessary software stack to execute face recognition experiments, but doesn't
provide any data to test it.
:ref:`Click here <databases-benchmark>` to see how to prepare the database data before execute an experiment.


Face recognition baselines are available in the format of `baseline <https://www.idiap.ch/software/bob/docs/bob/bob.bio.base/master/baseline.html>`_ via the command bellow::

  $ bob bio baseline <BASELINE_NAME> <DATABASE_NAME>

You can use `--help` for more information::

  $ bob bio baseline --help

To check it out the baselines and the databases available do::

  $ resources.py --types baseline
  $ resources.py --types database


Databases
=========

This subsection describes the databases used in this work and some of the state-of-the-art results.

.. toctree::
   :maxdepth: 1

   databases/databases_for_benchmark
   databases/databases_for_cnn


Baselines
=========

This subsection presents the error rate results for each baseline/database.

.. toctree::
   :maxdepth: 2

   baselines/baselines

Leaderboard
===========

.. toctree::
   :maxdepth: 2

   leaderboard



User guide
==========

.. toctree::
   :maxdepth: 2

   user_guide



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2

   references
