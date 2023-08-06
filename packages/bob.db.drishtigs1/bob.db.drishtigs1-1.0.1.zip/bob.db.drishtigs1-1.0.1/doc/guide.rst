.. -*- coding: utf-8 -*-

=============
User's Guide
=============

Setting up the Dataset
----------------------

Download the `Drishti-GS1 dataset`_, take note of it's root directory and configure the 
data access using the ``bob`` command-line configuration utility. For example:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob config set bob.db.drishtigs1.datadir /path/to/root/of/drishtigs1
    (your-bob-env) $ bob config show #to check


You can than check if your local version of the dataset is compatible with this interface 
and has the standard directory tree:

.. code-block:: sh

    $ conda activate your-bob-env
    (your-bob-env) $ bob_dbmanage.py dirshtigs1 checkfiles
    checkfiles completed sucessfully

Protocols 
---------

This packages provides the default protocol for optic disc and optic cup annotations as defined by the authors of the dataset:

1. "default_od" for optic disc
2. "default_cup" for the optic cup

.. note::

    Images have varying resolutions!


.. _drishti-gs1 dataset: http://cvit.iiit.ac.in/projects/mip/drishti-gs/mip-dataset2/Home.php