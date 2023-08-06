.. py:currentmodule:: bob.learn.pytorch

Conditional GAN
===============

The conditional GAN is an extension of the original GAN, by adding a conditioning variable
in the process. 
As an illustration, consider MNIST digits: instead of generating a digit between 0 and 9, the
condition variable would allow to generate a particular digit.

More particularly, the input to the generator (i.e. noise) will be 
concatenated with a variable specifying the particular condition to generate the fake data.
Also, there are different strategies to embed the conditioning variable in the discriminator.
Here we chose to concatenate the one-hot encoded conditional variable as feature maps to the
input image.

.. figure:: img/cond_map.png
   :align: center
    
   Conditional input to the discriminator

The article describing this algorithm is the following [cgan]_::

  @Misc{mirza-arxiv-2014,
    Author         = {Mirza, M. and Osindero, S.},
    Title          = {Conditional {G}enerative {A}dversarial {N}ets},
    eprint         = {arXiv:1411.1784},
    seq-number     = {49},
    year           = 2014
  }

There are other articles dealing specifically with conditional GANs for face processing, and this work is 
loosely based on `Conditional Generative Adversarial Nets for Convolutional Face Generation <http://www.foldl.me/uploads/papers/tr-cgans.pdf>`_
and inspired from the following `code <https://github.com/carpedm20/DCGAN-tensorflow>`_.
  
Here we consider the conditioning variable to be the pose of the face (in terms of yaw). We will
use the Multi-PIE database, since it contains face images with 13 different poses.

First of all, we need to write a configuration file, containing the dataset and the 
network definition:

.. code-block:: python

  ### DATA ###
  from bob.learn.pytorch.datasets.multipie import MultiPIEDataset
  from bob.learn.pytorch.datasets import RollChannels
  from bob.learn.pytorch.datasets import ToTensor
  from bob.learn.pytorch.datasets import Normalize
  import torchvision.transforms as transforms

  dataset = MultiPIEDataset(root_dir='path/to/multipie/data', 
                                   frontal_only=False, 
                                   transform=transforms.Compose([
                                     RollChannels(), 
                                     ToTensor(),
                                     Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                     ])
                                 )
  
  ### NETWORK ###
  from bob.learn.pytorch.architectures import ConditionalGAN_generator
  from bob.learn.pytorch.architectures import ConditionalGAN_discriminator
  from bob.learn.pytorch.architectures import weights_init

  noise_dim = 100
  conditional_dim = 13

  generator = ConditionalGAN_generator(noise_dim, conditional_dim)
  generator.apply(weights_init)
  discriminator = ConditionalGAN_discriminator(conditional_dim)
  discriminator.apply(weights_init)

.. note::

  You should have the ``bob.db.multipie`` package installed on your environment. Note also
  that this model acts on color images of face of size 64x64. It's up to you to preprocess
  your data to make them fit these constraints ...

To train the conditional GAN to generate faces with different poses, you should execute::

  $ ./bin/train_conditionalgan.py configuration.py -vv

If you have access to a GPU, you should run the script using this option::

  $ ./bin/train_conditionalgan.py configuration.py -vv --use-gpu

Generated samples will be saved after each training epoch. You can specify where to write
images using the ``--output-dir`` option (default to ``./conditionalgan``).

Here are some examples of generated face images with different poses:

.. figure:: img/cgan-multipie-epoch-1.png
   :align: center
    
   After 1 epoch

.. figure:: img/cgan-multipie-epoch-20.png
   :align: center
    
   After 20 epoch

.. figure:: img/cgan-multipie-epoch-50.png
   :align: center
    
   After 50 epoch

.. [cgan]  *M. Mirza, S. Osindero*. **Conditional Generative Adversarial Nets** `arXiv:1411.1784. <https://arxiv.org/abs/1411.1784>`__

