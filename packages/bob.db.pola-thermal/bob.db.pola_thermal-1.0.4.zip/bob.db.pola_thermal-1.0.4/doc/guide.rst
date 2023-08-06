.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Mon Oct 19 11:10:18 CEST 2015

==============
 User's Guide
==============

This package contains the access API and descriptions for the Polarimetric Thermal Database.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded by requesting the owners of the database.

The Database Interface
----------------------

The :py:class:`bob.db.pola_thermal.Database` complies with the standard biometric verification database as described in `bob.db.base <bob.db.base>`_, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`.


Polarimetric Thermal Database Protocols
---------------------------------------

In total we provide 11 evaluation protocols (each one split in 5 splits) and they are split in four macro groups.
To see all the possible protocols available in this dataset, please run the folowing code.

.. code-block:: python

   >>> import bob.db.pola_thermal
   >>> print bob.db.pola_thermal.Database().protocols()

For each protocol (and split) the 60 subjects are randomly split in such a way that 25 subjects are used for training and 35 subjects are used for testing ([HU2016]_).
The next subsections describes each macro group.


VIS-VIS protocol
================

The `VIS-VIS` protocol is a baseline for visible light experiments.
It uses the neutral expression images (**B**) for enrolment and expression images (**E**) for probing.
The training set (world) has images from both modalities.
To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.pola_thermal
   >>> db = bob.db.pola_thermal.Database()
   >>> #split_1
   >>> train = db.objects(protocol='VIS-VIS-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-VIS-split1', groups='dev', purposes="enroll")
   >>> test_probe = db.objects(protocol='VIS-VIS-split1', groups='dev', purposes="probe")
   >>>              


VIS-Overall protocols
=====================

The `VIS-Overall` protocols has heterogeneous comparisons already.
It uses **VIS** neutral expression images (**B**) for enrolment and, either thermal images (**S0**) or polarimetric thermal (**DoLP**) for probing.
The training set (world) has images from both modalities.

To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.pola_thermal
   >>> db = bob.db.pola_thermal.Database()
   >>>
   >>> # Thermal split_1
   >>> train = db.objects(protocol='VIS-thermal-overall-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-thermal-overall-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-thermal-overall-split1', groups='dev', purposes='probe')
   >>>              
   >>> # Polarimetric Thermal split_1
   >>> train = db.objects(protocol='VIS-polarimetric-overall-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-polarimetric-overall-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-polarimetric-overall-split1', groups='dev', purposes='probe')
   >>>              



VIS-Expression protocols
========================

The `VIS-Expression` protocols has heterogeneous comparisons.
It uses **VIS** neutral expression images (**B**) for enrolment.
For probing only images where the expression varies (**E**), either thermal (**S0**) or polarimetric (**DoLP**), are used.
The training set (world) has images from both modalities and all expressions.

To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.pola_thermal
   >>> db = bob.db.pola_thermal.Database()
   >>>
   >>> # Thermal split_1
   >>> train = db.objects(protocol='VIS-thermal-expression-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-thermal-expression-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-thermal-expression-split1', groups='dev', purposes='probe')
   >>>              
   >>> # Polarimetric Thermal split_1
   >>> train = db.objects(protocol='VIS-polarimetric-expression-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-polarimetric-expression-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-polarimetric-expression-split1', groups='dev', purposes='probe')
   >>>              



VIS-Range protocols
========================

The `VIS-Expression` protocols has heterogeneous comparisons.
It uses **VIS** neutral expression images (**B**) for enrolment.
For probing only images where the different ranges vary (**R1**, **R2** and **R3**), either thermal (**S0**) or polarimetric (**DoLP**), are used.
The training set (world) has images from both modalities and ranges.

To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.pola_thermal
   >>> db = bob.db.pola_thermal.Database()
   >>>
   >>> # Thermal - Range 1 - split_1
   >>> train = db.objects(protocol='VIS-thermal-R1-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-thermal-R1-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-thermal-R1-split1', groups='dev', purposes='probe')
   >>>              
   >>> # Polarimetric - Range 1 - split_1
   >>> train = db.objects(protocol='VIS-polarimetric-R1-split1', groups='world')
   >>> test_enroll = db.objects(protocol='VIS-polarimetric-R1-split1', groups='dev', purposes='enroll')
   >>> test_probe = db.objects(protocol='VIS-polarimetric-R1-split1', groups='dev', purposes='probe')
   >>>              


.. _bob: https://www.idiap.ch/software/bob
