=========================
Audio Embedding Extractor
=========================

This subpackage is part of ``bob.learn.pytorch``  package to extract features from an input audio using CNN models which
trained with pytorch_.

For this purpose, you can specify your feature extractor in configuration
file to be used together with the ``verifiy.py`` script from :ref:`bob.bio.base <bob.bio.base>`.


DltResNet Model
---------------


:ref:`bob.bio.base <bob.bio.base>` wrapper DltResNet model.


.. note::

   The models will automatically download to the data folder of this package and save it in
   ``[env-path]./bob/learn/pytorch/preprocessor/audio/data/drn34.pth.tar``.
   If you want to set another path for this model do::

   $ bob config set bob.learn.pytorch.extractor.audio.drn_modelpath /path/to/mymodel


ResNet Model
------------


:ref:`bob.bio.base <bob.bio.base>` wrapper ResNet model.


.. note::

   The models will automatically download to the data folder of this package and save it in
   ``[env-path]./bob/learn/pytorch/preprocessor/audio/data/rn34.pth.tar``.
   If you want to set another path for this model do::

   $ bob config set bob.learn.pytorch.extractor.audio.rn_modelpath /path/to/mymodel


A concrete example
------------------

Imagine that you have the DltResNet model and you would
like to use the embedding layer as a feature to encode identity.

Your ``preprocessor`` in bob_ pipe-lines should be defined this way in the configuration file:

.. code:: python

  from bob.learn.pytorch.preprocessor.audio import DltResNetExtractor

  _model = 'path/to/your/model.pth'
  _num_classes = 1211
  _use_res = False
  preprocessor = DltResNetExtractor(_model, _num_classes, use_res=_use_res)

Note that the number of classes is irrelevant here, but is required to build the
network (before loading it). ``_model``, ``_num_classes`` and ``_use_res`` are optional input arguments and will be set automatically. If you want to use ResNet model instead of DltResNet model, set the ``use_res`` input argument to ``True``. This class is the embedding extractor and this style of naming (``preprocessor``), is for compatibility with bob_ framework. In this set, we just need a dummy ``extractor`` in bob_ framework which can be defined in the configuration file in this way:

.. code:: python

  from bob.bio.base.extractor import CallableExtractor

  extractor = CallableExtractor(lambda x: x)
  extracted_directory = "preprocessed"
  skip_extraction = True


You can easily implement your own extractor based on your own network too. Just have
a look at the code in ``bob/learn/pytorch/preprocessor/audio``.


.. _bob: http://idiap.github.io/bob/
.. _pytorch: http://pytorch.org/
