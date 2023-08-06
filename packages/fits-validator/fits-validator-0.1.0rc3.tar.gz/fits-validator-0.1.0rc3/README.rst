DKIST Data Ingest Validator
===========================

An interface containing a validator and a generator of FITS header schemas with
schema implementations for DKIST specs:

- SPEC-0122 : Data received from the summit

- SPEC-214 : Data published by the Data Center (incomplete)

Features
--------

-  Uses `voluptuous <https://pypi.org/project/voluptuous/>`__ schemas to
   validate a given input header

-  3 keyword validations: type validation, required-ness validation, and value validation

-  Failure exceptions include a dictionary of validation failure causes


Installation
------------

.. code:: bash

   pip install fits-validator



Examples
--------


.. code:: python

    from fits_validator import spec122_validator, Spec122ValidationException

    try:
        spec122_validator('dkist_rosa0181200000_observation.fits')
    except Spec122ValidationException as e:
        print(e)

    #Errors during validation: errors={'PAC__007': 'expected str', 'ID___003': 'required key not provided', 'NAXIS3': 'required key not provided'}


This project is Copyright (c) AURA/NSO.
