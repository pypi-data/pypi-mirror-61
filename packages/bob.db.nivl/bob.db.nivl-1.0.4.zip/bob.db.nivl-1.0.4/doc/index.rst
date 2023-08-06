.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Mon Oct 19 11:10:18 CEST 2015

.. _bob.db.nivl:

===================================================
Near-Infrared and Visible-Light (NIVL) Dataset
===================================================

Collected by University of Notre Dame, the NIVL contains VIS and NIR face images from the same subjects.
The capturing process was carried out over the course of two semesters (fall 2011 and spring 2012). 
The VIS images were collected using a Nikon D90 camera. 
The Nikon D90 uses a 23.6x15.8 mm CMOS sensor and the resulting images have a 4288x2848 resolution.
The images were acquired using automatic exposure and automatic focus settings. 
All images were acquired under normal indoor lighting at about a 5-foot standoff with frontal pose and a neutral facial expression.

The NIR images were acquired using a Honeywell CFAIRS system.
CFAIRS uses a modified Canon EOS 50D camera with a 22.3x14.9 CMOS sensor. 
The resulting images have a resolution of 4770x3177. 
All images were acquired under normal indoor lighting with frontal pose and neutral facial expression. 
NIR images were acquired at both a 5ft and 7ft standoff.

The dataset contains a total of 574 subjects. 
There are a total of 2,341 VIS images and 22,264 NIR images from the 574 subjects. 
A total of 402 subjects had both VIS and NIR images acquired during at least one session during both the fall and spring semesters.
Both VIS and NIR images were acquired in the same session, although not simultaneously.

The informations above were extracted from:

.. code-block:: latex

  @article{bernhard2015NearIR,
    title={Near-IR to Visible Light Face Matching: Effectiveness of Pre-Processing Options for Commercial Matchers},
    author={Bernhard, John and Barr, Jeremiah and Bowyer, Kevin W and Flynn, Patrick},
    booktitle={IEEE Seventh International Conference on Biometrics: Theory, Applications and Systems},
    year={2015},
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

