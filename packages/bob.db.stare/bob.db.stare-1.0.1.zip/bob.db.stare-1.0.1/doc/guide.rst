.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `STARE dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.stare.datadir /path/to/root/of/stare
    (your-bob-env) $ bob config show #to check

You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py stare checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides a default protocol that uses the train/test split
as proposed in::

    @inproceedings{Man+16,
        author = {K.K. Maninis and J. Pont-Tuset and P. Arbel\'{a}ez and L. Van Gool},
        title = {Deep Retinal Image Understanding},
        booktitle = {Medical Image Computing and Computer-Assisted Intervention (MICCAI)},
        year = {2016}
    }

The first 10 images are used for training and the remaining 10 for testing.

.. _stare dataset: http://cecas.clemson.edu/~ahoover/stare/probing/index.html 
