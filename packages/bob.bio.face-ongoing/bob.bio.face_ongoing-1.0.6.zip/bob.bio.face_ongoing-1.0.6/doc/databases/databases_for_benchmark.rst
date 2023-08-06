.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


=========================
Databases for benchmarch
=========================
.. _databases-benchmark:

There are plenty of databases used for benchmarching face recognition systems.
So far, we are sticking with the ones below.


MOBIO
-----

The MOBIO database is a bi-modal (face/speaker) video database recorded from 152 people. 
The database has a female-male ratio of nearly 1:2 (100 males and 52 females) and was collected from August 2008 until July 2010 in 6 different sites from 5 different countries. 
In total 12 sessions were captured for each individual.

The database was recorded using two types of mobile devices: mobile phones (NOKIA N93i) and laptop computers (standard 2008 MacBook). 
In this paper we only use the mobile phone data. 
The MOBIO database is challenging since the data are acquired with uncontrolled illumination, facial expression, and face pose, and sometimes only parts of the face are visible.

Once this database is downloaded, edit the file `~/.bob_bio_databases.txt` and set the following variables::

  $  [YOUR_MOBIO_IMAGE_DIRECTORY] = /mobio/image/path
  $  [YOUR_MOBIO_ANNOTATION_DIRECTORY] = /mobio/annotations/path


IARPA Janus Benchmark A (IJB-A)
-------------------------------

The IJB-A database is a mixture of frontal and non-frontal images and videos (provided as single frames) from 500 different identities.
In many of the images and video frames, there are several people visible, but only the ones that are annotated with a bounding box should be taken into consideration.
For both model enrollment as well as for probing, images and video frames of one person are combined into so-called Templates.

The database is divided in 10 splits each defining training, enrollment and
probe data.

Once this database is downloaded, edit the file `~/.bob_bio_databases.txt` and set the following variables::

  $  [YOUR_IJBA_DIRECTORY] = /ijba/image/path


IARPA Janus Benchmark A (IJB-C)
-------------------------------

The IJB-C database is a mixture of frontal and non-frontal images and videos
(provided as single frames) from 3531 different identities. 
In many of the images and video frames, there are several people visible, but only the ones that are annotated with a bounding box should be taken into consideration.
For both model enrollment as well as for probing, images and video frames of one person are combined into so-called Templates.
For some of the protocols, probe templates are also generated from raw video data.

Once this database is downloaded, edit the file `~/.bob_bio_databases.txt` and set the following variables::

  $  [YOUR_IJBC_DIRECTORY] = /ijbc/image/path



Labeled Faces in the Wild Database
----------------------------------

Once this database is downloaded, edit the file `~/.bob_bio_databases.txt` and set the following variables::

  $  [YOUR_LFW_FUNNELED_DIRECTORY] = /lfw/image/path

