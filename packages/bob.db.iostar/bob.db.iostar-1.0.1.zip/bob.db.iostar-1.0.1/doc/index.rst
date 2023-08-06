.. -*- coding: utf-8 -*-

.. _bob.db.iostar:

===========================================
IOSTAR Retinal Vessel Segmentation Dataset
===========================================
This package is part of the signal-processing and machine learning toolbox Bob_. It provides an interface for the `IOSTAR Dataset`_. This package does
not contain the original data files, which need to be obtained through the link above.

The IOSTAR vessel segmentation dataset includes 30 images with a resolution of 1024 × 1024 pixels. 
All the vessels in this dataset are annotated by a group of experts working in the field of retinal image analysis. 
Additionally the dataset includes annotations for the optic disc and the artery/vein ratio.

If you use this package, please cite the authors of the database::

    @ARTICLE{7530915,
        author={J. {Zhang} and B. {Dashtbozorg} and E. {Bekkers} and J. P. W. {Pluim} and R. {Duits} and B. M. {ter Haar Romeny}},
        journal={IEEE Transactions on Medical Imaging},
        title={Robust Retinal Vessel Segmentation via Locally Adaptive Derivative Frames in Orientation Scores},
        year={2016},
        volume={35},
        number={12},
        pages={2631-2644},
        ISSN={0278-0062},
        month={Dec},
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _iostar dataset: http://www.retinacheck.org/download-iostar-retinal-vessel-segmentation-dataset