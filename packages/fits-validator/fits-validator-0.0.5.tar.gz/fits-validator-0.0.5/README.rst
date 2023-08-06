DKIST Data Ingest Validator
===========================


A pythonic interface containing a validator and a generator of FITS headers compliant with 
SPEC-0122 for DKIST data header validation testing at the Data Center. 

Features
--------

-  Use `voluptuous <https://pypi.org/project/voluptuous/>`__ schemas to 
   validate a given input header to the standard SPEC-0122 header schema

-  3 keyword validations: type validation, required-ness validation, and value validation

-  Returns a dictionary of ingest failure messages


Installation
------------

.. code:: bash

   pip install fits-validator



Examples
--------


.. code:: python


   from validator import FitsValidator

   val = FitsValidator()

   val.validate('dkist_rosa0181200000_observation.fits')
   #ValueError: Errors during Ingest Validation: {'PAC__007': 'expected str', 'ID___003': 'required key not provided', 'NAXIS3': 'required key not provided'}




This project is Copyright (c) AURA/NSO.