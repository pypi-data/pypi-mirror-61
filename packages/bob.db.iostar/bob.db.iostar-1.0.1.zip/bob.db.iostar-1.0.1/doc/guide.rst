.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `IOSTAR dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.iostar.datadir /path/to/root/of/iostar
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py iostar checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides two default protocols: \

1. ``default_vessel`` for binary vessel segmentation
2. ``default_od`` for binary optic disc segmentation

Each protocol uses the train/test split as proposed by Meyer et al. (2017)::

    @InProceedings{10.1007/978-3-319-59876-5_56,
        author="Meyer, Maria Ines
        and Costa, Pedro
        and Galdran, Adrian
        and Mendon{\c{c}}a, Ana Maria
        and Campilho, Aur{\'e}lio",
        editor="Karray, Fakhri
        and Campilho, Aur{\'e}lio
        and Cheriet, Farida",
        title="A Deep Neural Network for Vessel Segmentation of Scanning Laser Ophthalmoscopy Images",
        booktitle="Image Analysis and Recognition",
        year="2017",
        publisher="Springer International Publishing",
        address="Cham",
        pages="507--515",
        isbn="978-3-319-59876-5"
    }


The first 20 images are used for training and the remaining 10 for testing.


.. _iostar dataset: http://www.retinacheck.org/download-iostar-retinal-vessel-segmentation-dataset
