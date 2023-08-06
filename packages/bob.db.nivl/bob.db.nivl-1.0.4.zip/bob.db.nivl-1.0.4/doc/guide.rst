.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Mon Oct 19 11:10:18 CEST 2015

==============
 User's Guide
==============

This package contains the access API and descriptions for the Near-Infrared and Visible-Light (`NIVL`_) Dataset.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded from the original URL.

The Database Interface
----------------------

The :py:class:`bob.db.nivl.Database` complies with the standard biometric verification database as described in `bob.db.base <bob.db.base>`_, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`.


NIVL Protocols
---------------

In total we provide 14 evaluation protocols and they are split in three groups.
The next subsections will describe each group.


Original evaluation protocols
=============================

The goal of the original paper with the NIVL was to evaluate the error rates of commercial face recognition matchers under different image processing algorithms.
For that, the authors created two evaluation protocols.
With all the 574 subjects, (in one single set for evaluation) the first protocol matched NIR images from the spring 2012 acquisitions against the VIS images from fall 2011. 
The second protocol matched NIR images from the fall 2011 acquisitions against the VIS images from the spring 2012 acquisitions.
The both protocols are named as: ```original_2011-2012``` and ```original_2012-2011```.
To fetch the object files using these protocols use the following piece of code:

.. code-block:: python

   >>> import bob.db.nivl
   >>> db = bob.db.nivl.Database()
   >>> #original_2011-2012   
   >>> enrollment_data_2011 = db.objects(protocol='original_2011-2012', groups='eval', purposes="enroll")
   >>> probing_data_2011    = db.objects(protocol='original_2011-2012', groups='eval', purposes="probe")
   >>> 
   >>> #original_2012-2011   
   >>> enrollment_data_2012 = db.objects(protocol='original_2012-2011', groups='eval', purposes="enroll")
   >>> probing_data_2012    = db.objects(protocol='original_2012-2011', groups='eval', purposes="probe")
   >>>              


As it possible to see, these protocols do not provide a set for train algorithms.
For that reason, we developed the two other groups of protocols.


IDIAP comparison protocols
==========================

This group of protocols was designed to be a heterogeneous face **verification** reference.
The 574 clients were split in three groups called ```world```, ```dev``` and ```eval```.

The ```world``` set is composed by 229 clients and it is designed to be used as the training set.

The ```dev``` set is composed by 172 clients and it is designed to tune the hyper-parameters of a hererogeneous face recognition approach and to be the decision threshold reference.

The ```eval``` set is composed by 173 clients and it is used to assess the final unbiased system performance.

With that division we developed two protocols: ```idiap-comparison_2011-VIS-NIR``` and ```idiap-comparison_2012-VIS-NIR```.

In the ```idiap-comparison_2011-VIS-NIR```, VIS images from 2011 are used as enrollment and the NIR images (from both years) are used for probing.
To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.nivl
   >>> db = bob.db.nivl.Database()   
   >>> #Training set
   >>> train      = db.objects(protocol='idiap-comparison_2011-VIS-NIR', groups='world')   
   >>>
   >>> #Development set
   >>> dev_enroll = db.objects(protocol='idiap-comparison_2011-VIS-NIR', groups='dev', purposes="enroll")
   >>> dev_probe = db.objects(protocol='idiap-comparison_2011-VIS-NIR', groups='dev', purposes="probe")
   >>> 
   >>> #Evaluation set
   >>> eval_enroll = db.objects(protocol='idiap-comparison_2011-VIS-NIR', groups='eval', purposes="enroll")
   >>> eval_probe = db.objects(protocol='idiap-comparison_2011-VIS-NIR', groups='eval', purposes="probe")
   >>>              


In the ```idiap-comparison_2012-VIS-NIR```, VIS images from 2012 are used as enrollment and the NIR images (from both years) are used for probing.
To fetch the object files using this protocol use the following piece of code:

.. code-block:: python

   >>> import bob.db.nivl
   >>> db = bob.db.nivl.Database()   
   >>> #Training set
   >>> train      = db.objects(protocol='idiap-comparison_2012-VIS-NIR', groups='world')   
   >>>
   >>> #Development set
   >>> dev_enroll = db.objects(protocol='idiap-comparison_2012-VIS-NIR', groups='dev', purposes="enroll")
   >>> dev_probe = db.objects(protocol='idiap-comparison_2012-VIS-NIR', groups='dev', purposes="probe")
   >>> 
   >>> #Evaluation set
   >>> eval_enroll = db.objects(protocol='idiap-comparison_2012-VIS-NIR', groups='eval', purposes="enroll")
   >>> eval_probe = db.objects(protocol='idiap-comparison_2012-VIS-NIR', groups='eval', purposes="probe")
   >>>              


IDIAP search protocols
======================

This group of protocols was designed to be a heterogeneous face **identification** reference.
The 574 clients were split in two groups called ```world``` and ```dev```.

The ```world``` set is composed by 344 clients and it is designed to be used as the training set.

The ```dev``` set is composed by 230 clients and it is used to assess the final unbiased system performance.

With that division we developed two groups of protocols: ```idiap-search_2011-VIS-NIR_split[1-5]``` and ```idiap-search_2011-VIS-NIR_split[1-5]```.

In the ```idiap-search_2011-VIS-NIR_split[1-5]```, is composed by five splits ([1-5]) and the VIS images from 2011 are used as enrollment and the NIR images (from both years) are used for probing.
To fetch the object files using this protocol (let's say the first split) use the following piece of code:

.. code-block:: python

   >>> import bob.db.nivl
   >>> db = bob.db.nivl.Database()   
   >>> #Training set
   >>> train      = db.objects(protocol='idiap-search_2011-VIS-NIR_split1', groups='world')   
   >>>
   >>> #Evaluation set
   >>> dev_enroll = db.objects(protocol='idiap-search_2011-VIS-NIR_split1', groups='dev', purposes="enroll")
   >>> dev_probe = db.objects(protocol='idiap-search_2011-VIS-NIR_split1', groups='dev', purposes="probe")
   >>> 


In the ```idiap-search_2012-VIS-NIR_split[1-5]```, is composed by five splits ([1-5]) and the VIS images from 2012 are used as enrollment and the NIR images (from both years) are used for probing.
To fetch the object files using this protocol (let's say the first split) use the following piece of code:

.. code-block:: python

   >>> import bob.db.nivl
   >>> db = bob.db.nivl.Database()   
   >>> #Training set
   >>> train      = db.objects(protocol='idiap-search_2012-VIS-NIR_split1', groups='world')   
   >>>
   >>> #Evaluation set
   >>> dev_enroll = db.objects(protocol='idiap-search_2012-VIS-NIR_split1', groups='dev', purposes="enroll")
   >>> dev_probe = db.objects(protocol='idiap-search_2012-VIS-NIR_split1', groups='dev', purposes="probe")
   >>> 

.. _NIVL: http://www3.nd.edu/~kwb/publications.htm
.. _bob: https://www.idiap.ch/software/bob
