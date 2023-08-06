.. -*- coding: utf-8 -*-

.. _bob.db.chasedb1:

===============================
CHASE_DB1 Retinal Image Datbase
===============================
This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `CHASE_DB1 Dataset`_. This package does not contain 
the original data files, which need to be obtained through the link above.

The dataset contains 28 eye fundus images with a resolution of 1280 x 960. 
Two sets of ground-truth vessel annotations are available. The first set is commonly used for training and testing. 
The second set acts as a "human" baseline.

If you use this package, please cite the authors of the database::

    @ARTICLE{6224174,
        author={M. M. {Fraz} and P. {Remagnino} and A. {Hoppe} and B. {Uyyanonvara} and A. R. {Rudnicka} and C. G. {Owen} and S. A. {Barman}},
        journal={IEEE Transactions on Biomedical Engineering},
        title={An Ensemble Classification-Based Approach Applied to Retinal Blood Vessel Segmentation},
        year={2012},
        volume={59},
        number={9},
        pages={2538-2548},
        doi={10.1109/TBME.2012.2205687},
        ISSN={0018-9294},
        month={Sep.}
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _chase_db1 dataset: https://blogs.kingston.ac.uk/retinal/chasedb1/