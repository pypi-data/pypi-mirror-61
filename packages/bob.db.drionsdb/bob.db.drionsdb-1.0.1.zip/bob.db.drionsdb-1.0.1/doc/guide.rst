.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `DRIONS-DB dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.drionsdb.datadir /path/to/root/of/drionsdb
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py drionsdb checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides a default protocol that uses the train/test split
as proposed by::

    @inproceedings{Man+16,
        author = {K.K. Maninis and J. Pont-Tuset and P. Arbel\'{a}ez and L. Van Gool},
        title = {Deep Retinal Image Understanding},
        booktitle = {Medical Image Computing and Computer-Assisted Intervention (MICCAI)},
        year = {2016}
    }


The train-test split is defined on their `project website`_.  

.. _drions-db dataset: http://www.ia.uned.es/~ejcarmona/DRIONS-DB.html
.. _project website: http://www.vision.ee.ethz.ch/~cvlsegmentation/driu/downloads.html