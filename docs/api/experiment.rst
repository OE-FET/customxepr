
Experiment
==========

This section gives an overview of modules to handle and plot experimental EPR data.
It contains two modules: ``experiment.xepr_dataset`` defines classes to read, write,
manipulate and plot Xepr datasets from Bruker's BES3T file format.
``mode_picture_dataset.xepr_dataset`` defines classes to read, write and plot cavity mode
pictures.


This page documents the main classes available from ``experiment``. The full API is
documented in the pages for the respective submodules:

.. toctree::
   :maxdepth: 1

   mode_picture_dataset <mode_picture_dataset>
   xepr_dataset <xepr_dataset>


.. module:: experiment

.. autoclass:: XeprData
   :members:
   :show-inheritance:

.. autoclass:: XeprParam
   :members:
   :show-inheritance:

.. autoclass:: ModePicture
   :members:
