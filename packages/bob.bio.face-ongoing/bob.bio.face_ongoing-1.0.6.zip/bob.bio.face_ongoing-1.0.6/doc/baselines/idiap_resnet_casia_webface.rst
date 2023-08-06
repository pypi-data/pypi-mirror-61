.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


=====================================
Idiap - Resnet V2/V1 - Casia Webface
=====================================

Inspired by `**FaceNet** <https://github.com/davidsandberg/facenet>`_ we here at Idiap trained our own CNN using the Inception Resnet 2 architecture using Casia Webface database.
In this `links <https://gitlab.idiap.ch/bob/bob.bio.htface/blob/eb4f2f66723dc54d9fa5341f9bd46d3b3fe6b347/bob/bio/htface/config/tensorflow/CASIA_inception_resnet_v2_center_loss.py>`_ you can find the script that trains this neural network.

To trigger this training it's necessary to use the `bob.learn.tensorflow <http://gitlab.idiap.ch/bob/bob.learn.tensorflow/>`_ package and run the following command::

  $ ./bin/jman submit --name CELEB-GRAY --queue gpu -- bob_tf_train_generic CASIA_inception_resnet_v2_center_loss.py
  

Some quick details about this CNN (just as a mental note):

  - The hot encoded layer has 10574 neurons.
  - Faces were detected and croped to :math:`182 \times 182` using `MTCNN <https://gitlab.idiap.ch/bob/bob.ip.mtcnn>`_ face and landmark detector
  - The following data augmentation strategies were implemented:
     * Random crop to :math:`160 \times 160`
     * Random Flip
     * Images were normalized to have zero mean and standard deviation one
  - Learning rate of 0.1, 0.01, 0.001
  - RMSPROP Optimizer
  - Batch size of 90

