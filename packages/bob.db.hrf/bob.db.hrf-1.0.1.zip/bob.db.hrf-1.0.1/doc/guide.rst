.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `HRF dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.hrf.datadir /path/to/root/of/hrf
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py hrf checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides a default protocol that uses the train/test split
as proposed by::

    @ARTICLE{7420682,
        author={J. I. {Orlando} and E. {Prokofyeva} and M. B. {Blaschko}},
        journal={IEEE Transactions on Biomedical Engineering},
        title={A Discriminatively Trained Fully Connected Conditional Random Field Model for Blood Vessel Segmentation in Fundus Images},
        year={2017},
        volume={64},
        number={1},
        pages={16-27},
        doi={10.1109/TBME.2016.2535311},
        ISSN={0018-9294},
        month={Jan}
    }


The first five images of each category (healthy, diabtic retinopathy and glaucoma) are used for training 
and the remaining 30 for testing.

.. _hrf dataset: https://www5.cs.fau.de/research/data/fundus-images/
