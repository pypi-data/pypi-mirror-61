.. py:currentmodule:: bob.learn.pytorch

DCGAN
-----

DCGAN stands for deeply convolutional GAN, and is described in the following paper [dcgan]_::


  @InProceedings{radford-iclr-2016,
    Author         = {Radford, A. and Metz, L. and Chintala, S.},
    Title          = {Unsupervised {R}epresentation {L}earning with {D}eep
                   {C}onvolutional {G}enerative {A}dversarial {N}etworks},
    BookTitle      = {Intl {C}onf. on {L}earning {R}epresentation},
    seq-number     = {50},
    year           = 2016
  }

Also, most of the code (architecture and training) has been borrowed `here <https://github.com/pytorch/examples/tree/master/dcgan>`_.

Here, the goal is to generate images of frontal faces. You can train a model 
using the MULTI-PIE database by using the dedicated script, and a proper configuration 
file. The configuration file should be as follow:

.. code-block:: python


  ### DATA ###
  from bob.learn.pytorch.datasets.multipie import MultiPIEDataset
  from bob.learn.pytorch.datasets import RollChannels
  from bob.learn.pytorch.datasets import ToTensor
  from bob.learn.pytorch.datasets import Normalize
  import torchvision.transforms as transforms

  dataset = MultiPIEDataset(root_dir='path/to/multipie/data', 
                            frontal_only=True, 
                            transform=transforms.Compose([
                              RollChannels(), 
                              ToTensor(),
                              Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                             ])
                           )

  ### NETWORK ###
  from bob.learn.pytorch.architectures import DCGAN_generator
  from bob.learn.pytorch.architectures import DCGAN_discriminator
  from bob.learn.pytorch.architectures import weights_init

  ngpu = 1
  generator = DCGAN_generator(ngpu)
  generator.apply(weights_init)
  discriminator = DCGAN_discriminator(ngpu)
  discriminator.apply(weights_init)

.. note::

  You should have the ``bob.db.multipie`` package installed on your environment. Note also
  that this model acts on color images of face of size 64x64. It's up to you to preprocess
  your data to make them fit these constraints ...

Once your configuration file is done. You can learn a model to generate 
frontal face images by invoking the following script::

  $ ./bin/train_dcgan.py configuration.py -vv

If you have access to a GPU, you should run the script using this option::

  $ ./bin/train_dcgan.py configuration.py -vv --use-gpu


Note that this script will consider frontal faces only (but all illumination conditions).
Generated samples will be saved after each training epoch. You can specify where to write
images using the ``--output-dir`` option (default to ``./dcgan``).

Here are some examples of saved images.

.. figure:: img/dcgan-multipie-epoch-1.png
   :align: center
    
   After 1 epoch

.. figure:: img/dcgan-multipie-epoch-5.png
   :align: center
    
   After 5 epoch

.. figure:: img/dcgan-multipie-epoch-20.png
   :align: center
    
   After 20 epoch


.. [dcgan]  *A.Radford, L. Metz, S. Chintala*. **Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks** Intl Conf. on Learning Representation, 2016. `arXiv <https://arxiv.org/abs/1511.06434>`__
