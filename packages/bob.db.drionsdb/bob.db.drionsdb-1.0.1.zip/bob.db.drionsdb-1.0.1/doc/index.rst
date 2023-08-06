.. -*- coding: utf-8 -*-

.. _bob.db.drionsdb:

================================
DRIONS-DB Retinal Image Database
================================

This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `DRIONS-DB Dataset`_. This package does not contain 
the original data files, which need to be obtained through the link above.

The dataset contains 110 eye fundus images with a resolution of 600 x 400. 
Two sets of ground-truth optic disc annotations are available. The first set is commonly used for training and testing. 
The second set acts as a "human" baseline.

If you use this package, please cite the authors of the database::

    @article{Carmona:2008:ION:1383660.1383874,
        author = {Carmona, Enrique J. and Rinc\'{o}n, Mariano and Garc\'{\i}    a-Feijo\'{o}, Juli\'{a}n and Mart\'{\i}nez-de-la-Casa, Jos{\'e} M.},
        title = {Identification of the Optic Nerve Head with Genetic    Algorithms},
        journal = {Artif. Intell. Med.},
        issue_date = {July, 2008},
        volume = {43},
        number = {3},
        month = jul,
        year = {2008},
        issn = {0933-3657},
        pages = {243--259},
        numpages = {17},
        url = {http://dx.doi.org/10.1016/j.artmed.2008.04.005},
        doi = {10.1016/j.artmed.2008.04.005},
        acmid = {1383874},
        publisher = {Elsevier Science Publishers Ltd.},
        address = {Essex, UK},
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _drions-db dataset: http://www.ia.uned.es/~ejcarmona/DRIONS-DB.html