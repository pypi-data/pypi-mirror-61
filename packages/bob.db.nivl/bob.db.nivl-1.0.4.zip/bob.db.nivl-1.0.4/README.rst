.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu Apr 16 16:39:01 CEST 2015



.. image:: http://img.shields.io/badge/docs-v1.0.4-yellow.png
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.nivl/v1.0.4/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: http://beatubulatest.lab.idiap.ch/private/docs/bob/bob.db.nivl/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.cuhk_cufs/badges/v1.0.4/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nivl/commits/v1.0.4
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nivl
.. image:: http://img.shields.io/pypi/v/bob.db.nivl.png
   :target: https://pypi.python.org/pypi/bob.db.nivl
.. image:: https://img.shields.io/badge/original-data--files-a000a0.png
   :target: http://www3.nd.edu/~kwb/publications.htm


=======================================================
Near-Infrared and Visible-Light (NIVL) Dataset
=======================================================

This package contains the access API and descriptions for the `Near-Infrared and Visible-Light (NIVL) Dataset <http://www3.nd.edu/~kwb/face_recognition.htm>`.
The actual raw data for the database should be downloaded from the original URL.
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

NIVL is for research on VIS-NIR face recognition.
It includes 574 identities faces captured in both VIS and NIR.

  Bernhard, John, et al. "Near-IR to Visible Light Face Matching: Effectiveness of Pre-Processing Options for Commercial Matchers."

Installation
------------

Follow our `installation`_ instructions. Then, to install this package, run::

  $ conda install bob.db.nivl


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
