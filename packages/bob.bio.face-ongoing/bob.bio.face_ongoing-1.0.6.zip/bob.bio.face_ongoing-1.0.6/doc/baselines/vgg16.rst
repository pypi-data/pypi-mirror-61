.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


=====
VGG16
=====

The VGG-Face network model is made publicly available by the `Visual Geometry Group <www.robots.ox.ac.uk/~vgg/software/vgg_face>`_ at Oxford University.
Involving almost 135 million trainable parameters, this network has been shown to achieve a FR accuracy of 98.95\% on the LFW unrestricted.
VGG-Face is a CNN consisting of 16 hidden layers.
The initial 13 hidden layers are convolution and pooling layers, and the last three layers are fully-connected ('fc6', 'fc7', and 'fc8').
The input to this network is an appropriately cropped color face-image of pre-specified dimensions.

We use the representation produced by the 'fc7' layer of the VGG-Face CNN as a template for the input image.
When enrolling a client, the template produced by the VGG-Face network for each enrollment-sample is recorded.
For scoring, the network is used to generate a template for the probe face-image, which is then compared to the enrolled templates of the claimed identity using the Cosine-similarity measure.

Check it out `https://www.idiap.ch/software/bob/docs/bob/bob.bio.caffe_face/stable/index.html <https://www.idiap.ch/software/bob/docs/bob/bob.bio.caffe_face/stable/index.html>`_ for more information.


