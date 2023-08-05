Module for VEnCode-related projects based on FANTOM5 databases
==============================================================

This module contains classes and functions that perform intersectional genetics-related operations to find VEnCodes using databases provided by the `FANTOM5 consortium`_, namely the CAGE enhancer and transcription start site (TSS) databases.

For more information on the VEnCode technology, please refer to **Macedo and Gontijo, bioRxiv 2019. DOI:**

Getting started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

Prerequisites
^^^^^^^^^^^^^

To effectively use this module you will need Python3_ with the numpy, pandas, matplotlib and scipy libraries installed
in your machine.
Additionally, you will have to download the unannotated TSS files from `FANTOM5 consortium`_ website.

Installing
^^^^^^^^^^
1. Make sure you have the prerequisites;
2. Fork this project;
3. Change the location of the directory "Files" in this package to the parent directory.
4. Put the FANTOM5 TSS files in that directory called "Files".

Deployment
-----------------
To develop your own projects, import objects from .py files (internals.py) using, for example:

``from VEnCode import internals``

to then use in your own methods.
Note: You can see examples of most functions and objects being used by going to the "Scripts" folder. Old scripts can be found in somewhat obsolete directory Legacy Scripts.

Running the Tests
-----------------
Tests for this module can be run in several ways; some examples:

1. Run python's standard module "unittest" in the tests directory.
Basic example in command line:

``python -m unittest test_internals``

2. Install nosetests python package and run nosetests in the "tests" directory.
Basic example in command line:

``nosetests test_internals.py``

Contributing
------------

Please read `CONTRIBUTING.rst`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use SemVer_ for versioning. For the versions available, see the `tags on this repository`_.

Authors
-------

- `André Macedo`_
- Alisson Gontijo

See also the list of contributors_ who participated in this project.

License
-------

Refer to file LICENSE.

Acknowledgements
----------------
- Integrative Biomedicine Laboratory @ CEDOC, NMS, Lisbon (supported by FCT: UID/Multi/04462/2019; PTDC/MED-NEU/30753/2017; and PTDC/BIA-BID/31071/2017 and FAPESP: 2016/09659-3)
- CEDOC: Chronic Diseases Research Center, Nova Medical School, Lisbon
- The MIT Portugal Program (MITEXPL/BIO/0097/2017)
- LIGA PORTUGUESA CONTRA O CANCRO (LPCC) 2017.
- FCT (IF/00022/2012, SFRH/BD/94931/2013, PTDC/BEXBCM/1370/2014)
- Prof. Dr. Ney Lemke and Ms. Benilde Pondeca for important discussions.

.. Starting hyperlink targets:

.. _FANTOM5 consortium: http://fantom.gsc.riken.jp/5/data/
.. _Python3: https://www.python.org/
.. _SemVer: https://semver.org/
.. _tags on this repository: https://github.com/AndreMacedo88/VEnCode/tags
.. _CONTRIBUTING.rst: https://github.com/AndreMacedo88/VEnCode/blob/master/CONTRIBUTING.rst
.. _contributors: https://github.com/AndreMacedo88/VEnCode/graphs/contributors
.. _André Macedo: https://github.com/AndreMacedo88
