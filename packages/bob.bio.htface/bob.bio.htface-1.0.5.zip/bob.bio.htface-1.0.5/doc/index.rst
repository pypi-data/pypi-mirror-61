.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>

.. _bob.bio.htface:

===============================
 Heterogeneous Face Recognition
===============================

The goal of this package is to provide an "easy to reproduce" set of experiments in HETEROGENEOUS
face recognition databases.
This package is an extension of the
`bob.bio.base <https://www.idiap.ch/software/bob/docs/bob/bob.bio.base/stable/index.html>`_ framework.

Installation
============

The installation instructions are based on conda (**LINUX ONLY**).
Please `install conda <https://conda.io/docs/install/quick.html#linux-miniconda-install>`_ before continuing.

After everything installed do::

  $ conda install bob.bio.htface
  $ bob bio htface --help


If you want to **DEVELOP** this package, follow below one possible set of instructions::

  $ git clone https://gitlab.idiap.ch/bob/bob.bio.htface
  $ cd bob.bio.htface
  $ conda env create -f environment.yml
  $ source activate bob.bio.htface  # activate the environment
  $ buildout

.. warning::
  Before the magic begins, it's necessary to set a set of paths for the databases.
  Sorry, but there is no other way.
  Please, edit this file according to your own working environment::

  $ vim ~/.bobrc



Follow below how this file looks like::

    {
    "bob.bio.htface.experiment-directory": "[PATH-WHERE-THE-EXPERIMENTS-WILL-BE-EXECUTED]",

    "bob.bio.htface.cufs_path": "[CUHK-CUFS-DB-PATH]",
    "bob.bio.htface.arface_path": "[ARFACE-DB-PATH]",
    "bob.bio.htface.xm2vts_path": "[XM2VTS-DB-PATH]",
    "bob.bio.htface.cufs_extension": [".jpg", ".JPG", ".ppm"],

    "bob.bio.htface.nivl_path": "[NIVL-DB-PATH]",
    "bob.bio.htface.nivl_extension": ".png",

    "bob.bio.htface.polathermal_path": "[POLATHERMAL-DB-PATH]",
    "bob.bio.htface.polathermal_extension": ".png",

    "bob.bio.htface.casia_nir_vis_path": "[CBSR-NIR-VIS-2-DB-PATH]",
    "bob.bio.htface.casia_nir_vis_extension": [".bmp", ".jpg"],

    "bob.bio.htface.cufsf_path": "[CUHK-CUFSF-PATH]",
    "bob.bio.htface.feret_path": "[FERET-PATH]",
    "bob.bio.htface.cufsf_extension": [".jpg",".tif"],

    "bob.bio.face_ongoing.idiap_casia_inception_v1_centerloss_gray": "[INCEPTIONV1-GRAY-MODEL-PATH]",
    "bob.bio.face_ongoing.idiap_casia_inception_v1_centerloss_rgb": "[INCEPTIONV1-RGB-MODEL-PATH],
    "bob.bio.face_ongoing.idiap_casia_inception_v2_centerloss_gray": "[INCEPTIONV2-GRAY-MODEL-PATH],
    "bob.bio.face_ongoing.idiap_casia_inception_v2_centerloss_rgb": "[INCEPTIONV2-RGB-MODEL-PATH]

    }

.. warning::
  Sorry, but there is no other way, you have to set all these things

The task
========


The task of Heterogeneous Face Recognition consists in matching face images that are sensed in different domains, such as sketches to photographs (visual spectra images), thermal images to photographs or near-infrared images to photographs.

Follow below possible Heteregenous Face Recognition Scenarious.

.. image:: ./img/hfr_schema.png
 :scale: 100 %


Databases
=========

This subsection describes the databases used in this work.

.. toctree::
   :maxdepth: 2

   databases



Hypotheses
==========

.. toctree::
   :maxdepth: 2

   crafted_features
   session_variability
   gfk
   transfer_learning/transfer_learning


User guide
==========

.. toctree::
   :maxdepth: 2

   user_guide


References
==========
.. toctree::
   :maxdepth: 3

   references
