.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Mon Oct 19 11:10:18 CEST 2015

==============
 User's Guide
==============

This package contains the access API and descriptions for the CUHK Face Sketch FERET Database (`CUFSF`_) database.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded from the original URL.

The Database Interface
----------------------

The :py:class:`bob.db.cuhk_cufsf.Database`  complies with the standard biometric verification database as described in `bob.db.base <bob.db.base>`_, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`.


CUHK CUFSF Protocols
--------------------


For this database we developed two major blocks of protocols. One for face **identification** (search) and one for face **verification** (comparison).


Search protocols
================

Defines a set of protocols for VIS->Skectch and Sketch->VIS face identification (search) in a **close-set**.
These protocols were organized in the same way as in::

   @article{jin2015coupled,
     title={Coupled Discriminative Feature Learning for Heterogeneous Face Recognition},
     author={Jin, Yi and Lu, Jiwen and Ruan, Qiuqi},
     journal={Information Forensics and Security, IEEE Transactions on},
     volume={10},
     number={3},
     pages={640--652},
     year={2015},
     publisher={IEEE}
  }


For each task (VIS->Sketch or Sketch->VIS) the 1194 subjects are split in **5 sets** where:
 - 700 subjects are used for training
 - 494 subjects are used for evaluation

To fetch the object files using, lets say the first split for the VIS->sketch protocol, use the following piece of code:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufsf.Database()
   >>>
   >>> #fetching the files for training   
   >>> training = db.objects(protocol="search_split1_p2s", groups="world")
   >>>
   >>> #fetching the files for testing
   >>> galery =  db.objects(protocol="search_split1_p2s", groups="dev", purposes="enroll")
   >>> probes =  db.objects(protocol="search_split1_p2s", groups="dev", purposes="probe")
   >>>


To list the available protocols type:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufsf.Database()
   >>> print(db.protocols())


Comparison protocols
====================

Defines a set of protocols for VIS->Skectch and Sketch->VIS face verification (comparison).
These set of protocols were designed by IDIAP Research Institute team.

There is one protocol for each task (VIS->Sketch or Sketch->VIS) and, for each one, the 1194 subjects are split in:
 - 350 subjects are used for training
 - 350 subjects are used for development
 - 494 subjects are used for evaluation


To fetch the object files using, lets say the VIS->sketch comparison protocol, use the following piece of code:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufsf.Database()
   >>>
   >>> #fetching the files for training   
   >>> training = db.objects(protocol="idiap_verification_p2s", groups="world")
   >>>   
   >>> #fetching the files for development
   >>> galery_dev =  db.objects(protocol="idiap_verification_p2s", groups="dev", purposes="enroll")
   >>> probes_dev =  db.objects(protocol="idiap_verification_p2s", groups="dev", purposes="probe")
   >>>
   >>> #fetching the files for evaluation
   >>> galery_eval =  db.objects(protocol="idiap_verification_p2s", groups="eval", purposes="enroll")
   >>> probes_eval =  db.objects(protocol="idiap_verification_p2s", groups="eval", purposes="probe")
   >>>



.. _CUFSF: http://mmlab.ie.cuhk.edu.hk/archive/cufsf/
.. _bob: https://www.idiap.ch/software/bob
