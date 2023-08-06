.. -*- coding: utf-8 -*-

.. _bob.db.drive:

===========================================================
DRIVE: Digital Retinal Images for Vessel Extraction Dataset
===========================================================
This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `DRIVE Dataset`_. This package does not contain the
original data files, which need to be obtained through the link above.

The DRIVE database has been established to enable comparative studies on segmentation 
of blood vessels in retinal images. The set of 40 images has been divided into a training 
and a test set, both containing 20 images. For the training images, a single manual segmentation 
of the vasculature is available. For the test cases, two manual segmentations are available; 
one is used as gold standard, the other one can be used to compare computer generated 
segmentations with those of an independent human observer. All human observers that manually 
segmented the vasculature were instructed and trained by an experienced ophthalmologist.
They were asked to mark all pixels for which they were for at least 70% certain that they were vessel.

If you use this package, please cite the authors of the database::

    @article{staal:2004-855,
        author          = {J.J. Staal AND M.D. Abramoff AND M. Niemeijer AND M.A. Viergever AND B. van Ginneken},
        title           = {{Ridge based vessel segmentation in color images of the retina}},
        journal         = {{IEEE Transactions on Medical Imaging}},
        year            = {2004},
        volume          = {23},
        number          = {4},
        pages           = {501-509}
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _drive dataset: https://www.isi.uu.nl/Research/Databases/DRIVE/