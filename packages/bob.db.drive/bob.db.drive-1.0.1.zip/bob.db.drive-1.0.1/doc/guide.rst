.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `DRIVE dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.drive.datadir /path/to/root/of/drive
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py drive checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides a default protocol that uses the train/test split
as defined by the authors of the dataset.

.. _drive dataset: https://www.isi.uu.nl/Research/Databases/DRIVE/
