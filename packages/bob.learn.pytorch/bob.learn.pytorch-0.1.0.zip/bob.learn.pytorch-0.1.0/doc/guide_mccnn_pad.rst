.. py:currentmodule:: bob.learn.pytorch

======================================
Multi-Channel CNN (MCCNN) for face PAD
======================================


Training MCCNN for face PAD
===========================================================

This section gives a brief overview on training the multi-channel CNN framework for PAD. 
The framework described here is described in the publication [GMGNAM19]_. It is recommended to check the publication for better understanding of the framework. However, the framework present in this package does not exactly match with the one presented 
in the reference paper. The framework presented here is more flexible, can accomodate more channels, can subselect channels
to perform scalability study. The network implemented here replicates the network in multiple channels instead of sharing the common weights, this modification is made to perform experiments with adapting different channels easily (however, both implementations are functionally same). Another difference is the way data balancing is implemented. In the publication [GMGNAM19]_, databalancing is performed in the dataset using undersampling. However, in the current implementation, data imbalance in each mini-batch is handled explicitly by computing the weight for each samples and using it for the loss computation. 

Different stages for training MC-CNN are described below.

Preprocessing data
------------------

The dataloader for training MCCNN assumes the data is already preprocessed. The preprocessing can be done with ``spoof.py`` script from ``bob.pad.face`` package. The preprocessed files are stored in the location ``<PREPROCESSED_FOLDER>``.  Each 
file in the preprocessed folder contains ``.hdf5`` files which contains a FrameContainer with each frame being a multichannel
image with dimensions ``NUM_CHANNELSxHxW``.  Please refer to the section entitled *Multi-channel CNN for face PAD* in the
documentation of ``bob.pad.face`` package, for an explicit example on how to preprocess the data for training MCCNN.

Training MCCNN
--------------

All the parameters required to train MCCNN are defined in the configuration file ``config.py`` file. 
The ``config.py`` file should contain atleast the network definition and the dataset class to be used for training. 
It can also define the transforms, number of channels in mccnn, training parameters such as number of epochs, learning rate and so on.  

Structure of the config file
----------------------------

An example configuration file to train MCCNN with WMCA dataset is shown below

.. code-block:: python

    from torchvision import transforms

    from bob.learn.pytorch.architectures import MCCNN

    from bob.learn.pytorch.datasets import DataFolder

    from bob.pad.face.database import BatlPadDatabase

    from bob.learn.pytorch.datasets import ChannelSelect, RandomHorizontalFlipImage

    #==============================================================================
    # Load the dataset

    """ The steps are as follows

    1. Initialize a databae instance, with the protocol, groups and number of frames 
        (currently for the ones in 'bob.pad.face', and point 'data_folder_train' to the preprocessed directory )    
        Note: Here we assume that we have already preprocessed the with `spoof.py` script and dumped it to location 
        pointed to by 'data_folder_train'.

    2. Specify the transform to be used on the images. It can be instances of `torchvision.transforms.Compose` or custom functions.

    3. Initialize the `data_folder` class with the database instance and all other parameters. This dataset instance is used in
     the trainer class

    4. Initialize the network architecture with required arguments.

    5. Define the parameters for the trainer. 

    """

    #==============================================================================
    # Initialize the bob database instance 

    data_folder_train= <PREPROCESSED_FOLDER>

    output_base_path= <OUTPUT_PATH>

    extension='.h5'

    train_groups=['train'] # only 'train' group is used for training the network

    val_groups=['dev']

    do_crossvalidation=True
    #=======================

    if do_crossvalidation:
        phases=['train','val']
    else:
        phases=['train']

    groups={"train":['train'],"val":['dev']}

    protocols="grandtest-color-50"

    exlude_attacks_list=["makeup"]

    bob_hldi_instance = BatlPadDatabase(
        protocol=protocols,
        original_directory=data_folder_train,
        original_extension=extension,
        landmark_detect_method="mtcnn",  # detect annotations using mtcnn
        exclude_attacks_list=exlude_attacks_list,
        exclude_pai_all_sets=True,  
        append_color_face_roi_annot=False) 

    #==============================================================================
    # Initialize the torch dataset, subselect channels from the pretrained files if needed.

    SELECTED_CHANNELS = [0,1,2,3] 
    
    img_transform={}

    img_transform['train'] = transforms.Compose([ChannelSelect(selected_channels = SELECTED_CHANNELS),RandomHorizontalFlipImage(p=0.5),transforms.ToTensor()])

    img_transform['val'] = transforms.Compose([ChannelSelect(selected_channels = SELECTED_CHANNELS),transforms.ToTensor()])

    dataset={}

    for phase in phases:

        dataset[phase] = DataFolder(data_folder=data_folder_train,
                             transform=img_transform[phase],
                             extension='.hdf5',
                             bob_hldi_instance=bob_hldi_instance,
                             groups=groups[phase],
                             protocol=protocols,
                             purposes=['real', 'attack'],
                             allow_missing_files=True)


    #==============================================================================
    # Specify other training parameters

    NUM_CHANNELS = len(SELECTED_CHANNELS)

    ADAPTED_LAYERS = 'conv1-block1-group1-ffc'
    ADAPT_REF_CHANNEL = False

    batch_size = 32
    num_workers = 0
    epochs=25
    learning_rate=0.0001
    seed = 3
    use_gpu = False
    adapted_layers = ADAPTED_LAYERS
    adapt_reference_channel = ADAPT_REF_CHANNEL
    verbose = 2
    UID = "_".join([str(i) for i in SELECTED_CHANNELS])+"_"+str(ADAPT_REF_CHANNEL)+"_"+ADAPTED_LAYERS+"_"+str(NUM_CHANNELS)+"_"+protocols
    training_logs= output_base_path+UID+'/train_log_dir/'
    output_dir = output_base_path+UID


    #==============================================================================
    # Load the architecture

    assert(len(SELECTED_CHANNELS)==NUM_CHANNELS)

    network=MCCNN(num_channels = NUM_CHANNELS)
    #==============================================================================



Once the config file is defined, training the network can be done with the following code:

.. code-block:: sh

    ./bin/train_mccnn.py \                   # script used for MCCNN training
    config.py \                              # configuration file defining the MCCNN network, database, and training parameters
    -vv                                      # set verbosity level

People in Idiap can benefit from GPU cluster, running the training as follows:

.. code-block:: sh

    jman submit --queue gpu \                      # submit to GPU queue (Idiap only)
    --name <NAME_OF_EXPERIMENT> \                  # define the name of th job (Idiap only)
    --log-dir <FOLDER_TO_SAVE_THE_RESULTS>/logs/ \ # substitute the path to save the logs to (Idiap only)
    --environment="PYTHONUNBUFFERED=1" -- \        #
    ./bin/train_mccnn.py \                         # script used for MCCNN training
    config.py \                                    # configuration file defining the MCCNN network, database, and training parameters
    --use-gpu \                                    # enable the GPU mode
    -vv                                            # set verbosity level


For a more detailed documentation of functionality available in the training script, run the following command:

.. code-block:: sh

    ./bin/train_mccnn.py --help   # note: remove ./bin/ if buildout is not used

Please inspect the corresponding configuration file, ``wmca_mccn.py`` for example, for more details on how to define the database, network architecture and training parameters.

Running experiments with the trained model
------------------------------------------

The trained model file can be used with ``MCCNNExtractor`` to run PAD experiments with ``spoof.py`` script. A dummy algorithm is 
added to forward the scalar values computed as the final scores.

.. [GMGNAM19] *A. George, Z. Mostaani, D. Geissenbuhler, O. Nikisins, A. Anjos, S. Marcel*, **Biometric Face Presentation Attack Detection with Multi-Channel Convolutional Neural Network**,
            in: Submitted to: IEEE Transactions on Information Forensics & Security.

