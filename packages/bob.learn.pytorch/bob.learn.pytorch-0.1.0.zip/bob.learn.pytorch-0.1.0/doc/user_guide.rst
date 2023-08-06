===========
 User guide
===========

As the name suggest, this package makes heavy use of PyTorch_, so make sure you have it installed on your environment. 
It also relies on bob_ (and in particular for I/O and databases interfaces), so you may want to refer 
to their respective documentation as well. In particular, the following assumes that you have a conda environment
with bob installed (see `installation instructions <https://www.idiap.ch/software/bob/docs/bob/docs/stable/bob/doc/install.html>`_)
and that you cloned and built this package:

.. code-block:: bash
  
  $ git clone git@gitlab.idiap.ch:bob/bob.learn.pytorch.git
  $ cd bob.learn.pytorch
  $ buildout


Anatomy of the package
----------------------

This package is basically organized as follows (some files are omitted for clarity purposes):

.. code-block:: text

  bob/
  +-- learn/ 
      +-- pytorch/
          +-- architectures/
              +-- CNN8.py
              +-- CASIANet.py
              +-- ...
          +-- datasets/
              +-- casia_webface.py
              +-- multipie.py
              +-- ...
          +-- scripts/
              +-- train_cnn.py
              +-- ...
          +-- trainers/
              +-- CNNTrainer.py


+ ``architectures`` contains files defining the different network architectures. The network is defined as a derived class of :py:class:`torch.nn.Module` and must contain a ``forward`` method. See for instance the simple examples provided in `PyTorch documentation <https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html>`_.

+ ``datasets`` contains files implementing datasets as :py:class:`torch.utils.data.Dataset`. The dataset classes are meant to provide a bridge between bob's databases (i.e. ``bob.db.*``) and the dataset used by PyTorch. To see an example on how this could be achieved, have a look at ``bob/learn/pytorch/datasets/multipie.py``. This directory also contains some utility functions, such as wrappers around some `torchvision.transforms <https://pytorch.org/docs/stable/torchvision/transforms.html>`_ (note that this is needed since, some built-in ``torchvision.transforms`` ignore the labels).

+ ``scripts`` contains the various scripts to perform training. More on that below. 

+ ``trainers`` contains classes implementing training of networks. At the moment, there is only one trainer, which will train CNN for visual recognition. Note that the trainer may depend on the specific model (GANs, ...). 


Defining and training a network on an arbitrary dataset
-------------------------------------------------------

Now let's move to a concrete example. Let's say that the goal is to train a simple network to perform face recognition on the AT&T database.

First, you'll have to get the dataset, you can download it `here <http://www.cl.cam.ac.uk/Research/DTG/attarchive/pub/data/att_faces.zip>`_. Assuming that you downloaded the zip archive 
in your current directory, do the following:

.. code-block:: bash
  
  $ mkdir atnt
  $ unzip att_faces.zip -d atnt/ 
  $ rm atnt/README

The training script ``./bin/train_cnn.py`` has a config file as argument. 
The config file should specify **at least** the ``dataset`` and ``network`` variables (other parameters, such as the batch size could also be provided this way). 
Let's define the dataset: here we'll define it directly in a config file, but you can of course implement it in a separate file and import it. 
The following is heavily inspired by what is described in the `PyTorch tutorial on data laoding and processing <https://pytorch.org/tutorials/beginner/data_loading_tutorial.html>`_. 
Have a look there for more details.


.. code-block:: python

  import os
  import numpy

  # load images
  import bob.io.base
  import bob.io.image
  
  # to build your dataset
  from torch.utils.data import Dataset 
  
  # mainly use to compose transforms (i.e. apply more than one transform to an input image)
  import torchvision.transforms as transforms

  # wrapper around torchvision.transforms
  # turns out that the original ones are 'destroying' labels ...
  from bob.learn.pytorch.datasets import ToTensor
  from bob.learn.pytorch.datasets import Normalize
  from bob.learn.pytorch.datasets import Resize

  # to get the right number of classes (between 0 and n_classes)
  from bob.learn.pytorch.datasets.utils import map_labels
  
  
  
  class AtntDataset(Dataset):
    """ Class defining the AT&T face dataset as a PyTorch Dataset

    Attributes
    ----------
    root_dir: str
      The path to the raw images.
    transform: :py:mod:`torchvision.transforms`
      The transfrom to apply to the input image
    data_files: list(str)
      The list of image files.
    id_labels: list(int)
      The subjects' identity, for each file

    """
  def __init__(self, root_dir, transform=None):
    """ Init method

    Parameters
    ----------
    root_dir: str
      The path to the raw images.
    transform: :py:mod:`torchvision.transforms`
      The transfrom to apply to the input image

    """
    self.root_dir = root_dir
    self.transform = transform
    self.data_files = []
    id_labels = []

    for root, dirs, files in os.walk(self.root_dir):
      for name in files:
        filename = os.path.split(os.path.join(root, name))[-1]
        path = root.split(os.sep)
        subject = int(path[-1].replace('s', ''))
        self.data_files.append(os.path.join(root, name))
        id_labels.append(subject)

    self.id_labels = map_labels(id_labels)


  def __len__(self):
    """ Return the length of the dataset (i.e. nb of examples)
    """
    return len(self.data_files)


  def __getitem__(self, idx):
    """ Return a sample from the dataset
    
      The sample consists in an image and a label (i.e. a face and an ID)
    """
    image = bob.io.base.load(self.data_files[idx])

    # add an empty dimension so that the array is HxWxC (as expected by PyTorch)
    image = image[..., numpy.newaxis]
    identity = self.id_labels[idx]
    sample = {'image': image, 'label': identity}

    # apply transform
    if self.transform:
      sample = self.transform(sample)
    
    return sample

  # instantiate the dataset
  dataset = AtntDataset(root_dir='./atnt', 
                              transform=transforms.Compose([
                                Resize((32, 32)),
                                ToTensor(),
                                Normalize((0.5,), (0.5,))
                              ])
                             )



Now that we have a dataset, we should define a network. Again, we'll do it directly in the configuration file, but
you can also define it in ``architectures`` and import it in your configuration. For the sake of simplicity, the 
architecture is directly taken from `PyTorch tutorials <https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html>`_.
Note the slight modification at the end of the ``forward`` method: it returns both the ouput (``out``) and the 
*embedding* ``x`` (which may be used as a features to describe an identity).

.. code-block:: python

  import torch
  import torch.nn as nn
  import torch.nn.functional as F

  class Net(nn.Module):
  
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 40)


    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        out =  self.fc3(x)
        return out, x


    def num_flat_features(self, x):
        size = x.size()[1:]  
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
  
  # instantiate the network
  network = Net()


Since we have both a dataset and a network define in a configuration file, we can now train the 
network using the dataset. This is done by launching the following script on your terminal:

.. code-block:: bash
  
  $ ./bin/train_cnn config.py -vvv 

And the output should look like this:

.. code-block:: bash

  bob.learn.pytorch@2018-05-16 10:10:47,582 -- DEBUG: Model file = None
  bob.learn.pytorch@2018-05-16 10:10:47,582 -- DEBUG: Batch size = 64
  bob.learn.pytorch@2018-05-16 10:10:47,582 -- DEBUG: Epochs = 2
  bob.learn.pytorch@2018-05-16 10:10:47,583 -- DEBUG: Learning rate = 0.01
  bob.learn.pytorch@2018-05-16 10:10:47,583 -- DEBUG: Seed = 3
  bob.learn.pytorch@2018-05-16 10:10:47,583 -- DEBUG: Output directory = training
  bob.learn.pytorch@2018-05-16 10:10:47,583 -- DEBUG: Use GPU = False
  bob.learn.pytorch@2018-05-16 10:10:47,589 -- INFO: There are 400 training images from 39 categories
  bob.learn.pytorch@2018-05-16 10:10:47,589 -- INFO: Starting training from scratch
  bob.learn.pytorch@2018-05-16 10:10:47,851 -- INFO: [0/2][0/7] => Loss = 3.6826722621917725 (time spent: 0.11152887344360352)
  bob.learn.pytorch@2018-05-16 10:10:48,010 -- INFO: [0/2][1/7] => Loss = 3.7005279064178467 (time spent: 0.01898503303527832)
  bob.learn.pytorch@2018-05-16 10:10:48,165 -- INFO: [0/2][2/7] => Loss = 3.6845760345458984 (time spent: 0.014686822891235352)
  bob.learn.pytorch@2018-05-16 10:10:48,337 -- INFO: [0/2][3/7] => Loss = 3.698812246322632 (time spent: 0.01413273811340332)
  bob.learn.pytorch@2018-05-16 10:10:48,479 -- INFO: [0/2][4/7] => Loss = 3.6925580501556396 (time spent: 0.013530492782592773)
  bob.learn.pytorch@2018-05-16 10:10:48,731 -- INFO: [0/2][5/7] => Loss = 3.6884894371032715 (time spent: 0.015494346618652344)
  bob.learn.pytorch@2018-05-16 10:10:48,839 -- INFO: [0/2][6/7] => Loss = 3.701101303100586 (time spent: 0.008399486541748047)
  bob.learn.pytorch@2018-05-16 10:10:48,839 -- INFO: EPOCH 1 DONE
  bob.learn.pytorch@2018-05-16 10:10:48,839 -- INFO: Saving model to training/model_1_0.pth
  bob.learn.pytorch@2018-05-16 10:10:49,084 -- INFO: [1/2][0/7] => Loss = 3.6887857913970947 (time spent: 0.01661086082458496)
  bob.learn.pytorch@2018-05-16 10:10:49,470 -- INFO: [1/2][1/7] => Loss = 3.690291404724121 (time spent: 0.20917153358459473)
  bob.learn.pytorch@2018-05-16 10:10:49,653 -- INFO: [1/2][2/7] => Loss = 3.690778970718384 (time spent: 0.018873929977416992)
  bob.learn.pytorch@2018-05-16 10:10:49,814 -- INFO: [1/2][3/7] => Loss = 3.7087666988372803 (time spent: 0.015717029571533203)
  bob.learn.pytorch@2018-05-16 10:10:50,022 -- INFO: [1/2][4/7] => Loss = 3.684515953063965 (time spent: 0.02263784408569336)
  bob.learn.pytorch@2018-05-16 10:10:50,253 -- INFO: [1/2][5/7] => Loss = 3.6845874786376953 (time spent: 0.014308452606201172)
  bob.learn.pytorch@2018-05-16 10:10:50,306 -- INFO: [1/2][6/7] => Loss = 3.6927332878112793 (time spent: 0.008508920669555664)
  bob.learn.pytorch@2018-05-16 10:10:50,306 -- INFO: EPOCH 2 DONE
  bob.learn.pytorch@2018-05-16 10:10:50,306 -- INFO: Saving model to training/model_2_0.pth


Congrats ! You have successfully train your first model (it is meaningless though ...).


A more realistic example
------------------------

.. note::

  For this example to work, you should first download the `CASIA Webface database <http://www.cbsr.ia.ac.cn/english/CASIA-WebFace-Database.html>`_,
  detect, crop and resize color face images to 128x128 ...

Imagine now that you want to try and reproduce what is described in the following article:

.. code-block:: latex

  @Misc{yi-arxiv-2014,
    Author         = {Yi, D. and Lei, Z. and Liao, S. and Li, S.Z.},
    Title          = {Learning Face Representation From Scratch},
    eprint         = {arXiv:1411.7923},
    year           = 2014
  }

Your configuration file ``casia.py`` should look like:

.. code-block:: python

  ### DATA ###
  from bob.learn.pytorch.datasets import CasiaWebFaceDataset
  import torchvision.transforms as transforms
  from bob.learn.pytorch.datasets import RollChannels
  from bob.learn.pytorch.datasets import ToTensor
  from bob.learn.pytorch.datasets import Normalize
  dataset = CasiaWebFaceDataset(root_dir='/path-to-your-cropped-faces-images', 
                                       transform=transforms.Compose([
                                         RollChannels(), 
                                         ToTensor(),
                                         Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                       ])
                                     )

  ### NETWORK ###
  from bob.learn.pytorch.architectures import CASIANet
  number_of_classes = 10575
  dropout = 0.5
  network = CASIANet(number_of_classes, dropout)

Then, you can lauch the trainin script (and leave it running for one week or so ...)

.. code-block:: bash
  
  $ ./bin/train_cnn casia.py -vvv 



.. _bob: http://idiap.github.io/bob/
.. _pytorch: http://pytorch.org/


