.. vim: set fileencoding=utf-8 :

.. _bob.db.oulunpu:

=================================
 OULU-NPU Database Access in Bob
=================================

This package provides an interface to the `OULU-NPU`_ - a mobile face
presentation attack database with real-world variations database. The original
data files need to be downloaded separately.After you have downloaded the
dataset, you need to configure bob.db.oulunpu to find the dataset::

    $ bob config set bob.db.oulunpu.directory /path/to/downloaded/dataset

Please see Bob's :ref:`bob.extension.rc` for more information about the ``bob config``
command.

If you use this database, please cite the following publication::

    @INPROCEEDINGS{OULU_NPU_2017,
             author = {Boulkenafet, Z. and Komulainen, J. and Li, Lei. and Feng, X. and Hadid, A.},
           keywords = {biometrics, face recognition, anti-spoofing, presentation attack, generalization, colour texture},
              month = May,
              title = {{OULU-NPU}: A mobile face presentation attack database with real-world variations},
            journal = {IEEE International Conference on Automatic Face and Gesture Recognition},
               year = {2017},
    }


Package Documentation
---------------------

.. automodule:: bob.db.oulunpu
.. _oulu-npu: https://sites.google.com/site/oulunpudatabase/

