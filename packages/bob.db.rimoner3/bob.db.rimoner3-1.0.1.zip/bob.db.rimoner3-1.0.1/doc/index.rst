.. -*- coding: utf-8 -*-

.. _bob.db.rimoner3:

=========================================
RIM-ONE Release 3 
=========================================

This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `RIM-ONE r3 Dataset`_. This package does not contain 
the original data files, which need to be obtained through the link above.

The dataset contains 159 stereo eye fundus images with a resolution of 2144 x 1424. The right 
part of the stereo image is disregarded. Two sets of ground-truths for optic disc and optic 
cup are available. The first set is commonly used for training and testing. The second set acts 
as a "human" baseline.

If you use this package, please cite the authors of the database::

    @inproceedings{inproceedings,
        author = {Fumero, Francisco and Sigut, Jose and Alayón, Silvia  andGonzález-Hernández, M and González de la Rosa, M},
        year = {2015},
        month = {06},
        pages = {},
        title = {Interactive Tool and Database for Optic Disc and   CupSegmentation of Stereo and Monocular Retinal Fundus Images}
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _rim-one r3 dataset: http://medimrg.webs.ull.es/research/retinal-imaging/rim-one/