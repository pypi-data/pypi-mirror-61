.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


==============================
Databases used to train models
==============================

Several face recognition databases are released by year by the community interested in this research.
Among them, some are claimed to be large scale, with huge amounts of identities and samples.
Such databases are very suitable to train "robust" models, mostly neural networks.

Here we focus in 3 databases.


Casia Webface
-------------

This database contains 494,414 face images of 10,575 identities.

.. Todo:: Provide some statistics about this dataset (e.g. number of samples per identity)


MSCeleba
--------

The `MS-Celeb 1M <http://www.msceleb.org/>`_ has around 10M images of 100K identities.
This dataset has several issues with mislabeling.
We implemented a prunning algorithm using the DBScan clustering.

.. Todo:: Provide some statistics about this dataset (e.g. number of samples per identity)


MegaFace 2
----------

The `MegaFace 2 <http://megaface.cs.washington.edu/participate/challenge2.html>`_ has arond 4M samples of 672K identities.


.. Todo:: Provide some statistics about this dataset (e.g. number of samples per identity)


