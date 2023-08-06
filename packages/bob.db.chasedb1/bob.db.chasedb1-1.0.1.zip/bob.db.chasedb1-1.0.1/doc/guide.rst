.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `CHASE_DB1 dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.chasedb1.datadir /path/to/root/of/chasedb1
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py chasedb1 checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides a default protocol that uses the train/test split
as proposed by the authors of the dataset. The first 8 images are used 
for training and the remaining 20 for testing.

.. _chase_db1 dataset: https://blogs.kingston.ac.uk/retinal/chasedb1/
