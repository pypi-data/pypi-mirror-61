.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Fri 20 Nov 2015 16:54:53 CET 

.. _bob.db.cuhk_cufsf:

=======================================
CUHK Face Sketch FERET Database (CUFSF)
=======================================

This package contains the access API and descriptions for the `CUHK Face Sketch FERET Database (CUFSF) <http://mmlab.ie.cuhk.edu.hk/archive/cufsf/>`. 
The actual raw data for the database should be downloaded from the original URL. 
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

.. image:: ./img/cufsf.jpg 
   :scale: 25

CUHK Face Sketch FERET Database (CUFSF) is for research on face sketch synthesis and face sketch recognition.
It includes 1194 faces from the FERET database with their respective sketches (drawn by an artist based on a photo of the FERET database).

If you use this package, please cite the authors of the database::

   @inproceedings{zhang2011coupled,
     title={Coupled information-theoretic encoding for face photo-sketch recognition},
     author={Zhang, Wei and Wang, Xiaogang and Tang, Xiaoou},
     booktitle={Computer Vision and Pattern Recognition (CVPR), 2011 IEEE Conference on},
     pages={513--520},
     year={2011},
     organization={IEEE}
   }



Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

