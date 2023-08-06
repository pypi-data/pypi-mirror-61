.. -*- coding: utf-8 -*-

.. _bob.db.stare:

===============================================
STARE STructured Analysis of the Retina Dataset
===============================================
This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `STARE Dataset`_. This package does not contain 
the original data files, which need to be obtained through the link above.

The dataset contains 20 eye fundus images with a resolution of 700 x 605. 
Two sets of ground-truth vessel annotations are available. The first set by Adam Hoover is commonly used for training and testing. 
The second set by Valentina Kouznetsova acts as a "human" baseline.

If you use this package, please cite the authors of the database::

    @ARTICLE{845178,
        author={A. D. {Hoover} and V. {Kouznetsova} and M. {Goldbaum}},
        journal={IEEE Transactions on Medical Imaging},
        title={Locating blood vessels in retinal images by piecewise threshold probing of a matched filter response},
        year={2000},
        volume={19},
        number={3},
        pages={203-210},
        doi={10.1109/42.845178},
        ISSN={0278-0062},
        month={March},
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _stare dataset: http://cecas.clemson.edu/~ahoover/stare/probing/index.html