Module for VEnCode-related projects based on FANTOM5 databases
==============================================================

This module contains classes and functions that perform intersectional genetics-related operations to find VEnCodes using databases provided by the `FANTOM5 consortium`_, namely the CAGE enhancer and transcription start site (TSS) databases.

For more information on the VEnCode technology, please refer to **Macedo and Gontijo, bioRxiv 2019. DOI:10.1101/552984**

Getting started
---------------

These instructions are designed to:

- Get you a copy of the project up and running on your local machine for development and testing purposes;
- Install the VEnCode package in your python library environment for use in your projects.

Prerequisites
^^^^^^^^^^^^^

To effectively use this module you will need Python3_ with some external libraries installed in your machine.
Check the requirements_ file.
If you install the package with pip, it should resolve the library requirements for you.

Additionally, you will have to download the unannotated TSS files from `FANTOM5 consortium`_ website.
More specifically, for human, `this file`_ for promoter analysis, and `this one`_ and the `ID-sample name`_ map for enhancers.
Finally, download the `curated sample category file`_.

Those 4 files are enough to find CAGE-based VEnCodes for human.

Installing
^^^^^^^^^^
1. Make sure you have the prerequisites;

If you want to edit the project:

2. Fork this project;
3. Put the missing FANTOM5 prerequisite files (only the large TSS files are missing) in the directory called "Files".

If you are a user:

2. Install VEnCode with pip;
3. Put all the FANTOM5 prerequisite files in a directory of your choice and when creating DataTpm objects remember to pass the argument: files_path=your_dir_path.

Deployment
-----------------
To develop your own projects, import objects directly from VEnCode using, for example:

.. code-block:: python

    import VEnCode
    object1 = VEnCode.DataTpm(...)

You can see examples of some functions and objects being used at the VEnCode capsule hosted in CodeOcean.

Alternatively, you can look at more advanced usage by going to the "Scripts" folder inside the package.

Running the Tests
-----------------
Tests for this module can be run in several ways; some examples:

1. In the command-line:

1.1. Run python's standard module "unittest" in the tests directory.
Basic example in command line:

.. code-block:: console

    python -m unittest test_internals

1.2. Install nosetests python package and run nosetests in the "tests" directory.
Basic example in command line:

.. code-block:: console

    nosetests test_internals.py

2. By importing the VEnCode module in python:

.. code-block:: python

    from VEnCode import tests
    tests.test_internals_()

Contributing
------------

Please read `CONTRIBUTING.rst`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use SemVer_ for versioning. For the versions available, see:

- The `tags on github`_, or
- In the PyPi_

Authors
-------

- `Andre Macedo`_
- `Alisson M. Gontijo`_

See also the list of contributors_ who participated in this project.

License
-------

Refer to file LICENSE_.

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
.. _this file: https://fantom.gsc.riken.jp/5/datafiles/latest/extra/CAGE_peaks/hg19.cage_peak_phase1and2combined_tpm.osc.txt.gz
.. _this one: https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Enhancers/human_permissive_enhancers_phase_1_and_2_expression_tpm_matrix.txt.gz
.. _ID-sample name: https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Enhancers/Human.sample_name2library_id.txt
.. _curated sample category file: https://github.com/AndreMacedo88/VEnCode/blob/master/VEnCode/Files/sample%20types%20-%20FANTOM5.csv
.. _Python3: https://www.python.org/
.. _requirements: https://github.com/AndreMacedo88/VEnCode/blob/master/requirements.txt
.. _SemVer: https://semver.org/
.. _tags on github: https://github.com/AndreMacedo88/VEnCode/tags
.. _PyPi: https://pypi.org/project/VEnCode/#history
.. _CONTRIBUTING.rst: https://github.com/AndreMacedo88/VEnCode/blob/master/CONTRIBUTING.rst
.. _contributors: https://github.com/AndreMacedo88/VEnCode/graphs/contributors
.. _Andre Macedo: https://github.com/AndreMacedo88
.. _Alisson M. Gontijo: https://github.com/alissongontijo
.. _LICENSE: https://github.com/AndreMacedo88/VEnCode/blob/master/LICENSE
