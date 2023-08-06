.. -*- coding: utf-8 -*-

.. _bob.db.hrf:

=========================================
HRF High-Resolution Fundus Image Database
=========================================

This package is part of the signal-processing and machine learning toolbox Bob_. 
It provides an interface for the `HRF Dataset`_. This package does not contain 
the original data files, which need to be obtained through the link above.

The dataset contains 45 eye fundus images with a resolution of 3304 x 2336. 
One set of ground-truth vessel annotations is available.

If you use this package, please cite the authors of the database::

    @ARTICLE{budai_robust_2013,
        title = {Robust {Vessel} {Segmentation} in {Fundus} {Images}},
        url = {https://www.hindawi.com/journals/ijbi/2013/154860/},
        language = {en},
        urldate = {2018-02-03},
        journal = {International Journal of Biomedical Imaging},
        author = {Budai, A. and Bock, R. and Maier, A. and Hornegger, J. and Michelson, G.},
        year = {2013},
        pmid = {24416040},
        doi = {10.1155/2013/154860},
    }

.. toctree::
   :maxdepth: 2
   
   guide
   py_api

.. todolist::

.. include:: links.rst
.. _hrf dataset: https://www5.cs.fau.de/research/data/fundus-images/