.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `REFUGE dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.refuge.datadir /path/to/root/of/refuge
    (your-bob-env) $ bob config show #to check

You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py refuge checkfiles
    checkfiles completed sucessfully

Protocols 
---------

A total of 1200 color fundus photographs are available. All fundus images are stored as JPEG files. 
The dataset is split 1:1:1 into 3 subsets equally for training, offline validation and onsite test, 
stratified to have equal glaucoma presence percentage. Training set with a total of 400 color fundus
image will be provided together with the corresponding glaucoma status and the unified manual 
pixel-wise annotations (a.k.a. ground truth). Testing consists of 800 color fundus images and is 
further split into 400 off-site validation set images and 400 on-site test set images. The two default protocols are:

1. "default_od" for optic disc
2. "default_cup" for the optic cup

The images are acquired with two different fundus cameras: 

- Zeiss Visucam 500 (2124x2056 pixels) - For Training
- Canon CR-2 (1634x1634 pixels) - For Validation and Test

.. note::

    Train and Test images have different resolutions!

.. _refuge dataset: http://ai.baidu.com/broad/download?dataset=gon
