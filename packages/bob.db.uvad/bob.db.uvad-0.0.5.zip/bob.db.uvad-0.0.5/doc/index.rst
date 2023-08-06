.. vim: set fileencoding=utf-8 :

.. _bob.db.uvad:

=================================
 UVAD Database Access in Bob
=================================

This package provides an interface to the Unicamp Video-Attack Database
(`UVAD`_) database. The original data files need to be downloaded separately.
After you have downloaded the dataset, you need to configure bob.db.uvad to
find the dataset::

    $ bob config set bob.db.uvad.directory /path/to/downloaded/dataset

If you use this database, please cite the following publication::

    @ARTICLE{7017526,
    author={Pinto, A. and Robson Schwartz, W. and Pedrini, H. and De Rezende Rocha, A.},
    journal={Information Forensics and Security, IEEE Transactions on},
    title={Using Visual Rhythms for Detecting Video-Based Facial Spoof Attacks},
    year={2015},
    month={May},
    volume={10},
    number={5},
    pages={1025-1038},
    keywords={Authentication;Biometrics (access control);Databases;Face;Feature extraction;Histograms;Noise;Unicamp Video-Attack Database;Video-based Face Spoofing;Video-based face spoofing;Visual Rhythm, Video-based Attacks;impersonation detection in facial biometric systems;unicamp video-attack database;video-based attacks;visual rhythm},
    doi={10.1109/TIFS.2015.2395139},
    ISSN={1556-6013},}

Package Documentation
---------------------

.. automodule:: bob.db.uvad
.. _uvad: http://ieeexplore.ieee.org/abstract/document/7017526/

