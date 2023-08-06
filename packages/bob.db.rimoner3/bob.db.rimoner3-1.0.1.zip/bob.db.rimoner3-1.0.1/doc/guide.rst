.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `RIM-ONE r3 dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.rimoner3.datadir /path/to/root/of/rimoner3
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py rimoner3 checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides two default protocols: \

1. ``default_od`` for binary optic disc segmentation
2. ``default_cup`` for binary optic cup segmentation

that uses the train/test split as proposed by::

    @inproceedings{Man+16,
        author = {K.K. Maninis and J. Pont-Tuset and P. Arbel\'{a}ez and L. Van Gool},
        title = {Deep Retinal Image Understanding},
        booktitle = {Medical Image Computing and Computer-Assisted Intervention (MICCAI)},
        year = {2016}
    }


The train-test split is defined on their `project website`_.  


.. _rim-one r3 dataset: http://medimrg.webs.ull.es/research/retinal-imaging/rim-one/
.. _project website: http://www.vision.ee.ethz.ch/~cvlsegmentation/driu/downloads.html