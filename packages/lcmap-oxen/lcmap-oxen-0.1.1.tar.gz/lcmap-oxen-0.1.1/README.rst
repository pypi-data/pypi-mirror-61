lcmap-oxen
==========
Tooling for creating the auxiliary datasets needed in LCMAP

Installing
----------

.. code-block:: bash

    pip install lcmap-oxen

A full GDAL installation is required.  GDAL can be compiled and installed by conda.
    

Other requirements:
-------------------

python >= 3.6


Run the script from the command line:
-------------------------------------

.. code-block:: bash

    $ clip_nlcd -i /path/to/conus-nlcd-raster -o /path/to/output-directory/ --acquired YYYYMMDD --prod NLCD *or* NLCD_TRAINING

   
CLI parameters:
---------------

* -i, The full path to a CONUS NLCD raster file.
* -o, The full path to an output directory, will be created if it does not exist.
* --acquired, A date (YYYYMMDD) that describes the acquisition of the original raster data; used in the filenames for the outputs.
* --prod, A string description of the input dataset, currently NLCD and NLCD_TRAINING are valid options; used in the filenames for the outputs.
* --overwrite, Optional, adding this will cause existing files to be overwritten, otherwise they will be skipped.

This script was designed to generate tiled NLCD but could be modified to produce other tiled LCMAP auxiliary products.
