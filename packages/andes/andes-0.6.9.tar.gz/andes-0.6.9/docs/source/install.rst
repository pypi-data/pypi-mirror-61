.. _install:

*************************
Installation instructions
*************************

User Mode Installation
======================
Conda Installation for Windows, macOS and Linux
***********************************************
ANDES can be installed in Python 3.7+. We recommend the Miniconda distribution
that includes the conda package manager and Python.
Downloaded and install the latest Miniconda (x64, with Python 3)
from https://conda.io/miniconda.html.

Open the Anaconda Prompt and create an environment for ANDES (optional)

.. code:: bash

     conda create --name andes python=3.7
     activate andes

Add the conda-forge channel and set it as default

.. code:: bash

     conda config --add channels conda-forge
     conda config --set channel_priority flexible

Install ANDES from conda-forge

.. code:: bash

     conda install andes

Existing Python Environment Installation
****************************************

If you prefer to use an existing Python installation,
you can install ANDES with `pip`

.. code:: bash

      python3 -m pip install andes

Pip will take care of the minimal dependency for ANDES.
The following package installation are also recommended

.. code:: bash

      python3 -m pip install matplotlib pandas sympy cvxpy flask requests

If you see a `Permission denied` error, you may need to
install the packages locally with `--user`

Development Mode
================
Alternative to installing as a distribution package, you may install ANDES
in development mode so that your changes will take effect immediately.

We still recommend you install ANDES with conda first. Then, remove the ANDES
package while preserving the dependent package with ::

      conda remove andes --force

Next, clone the ANDES source code from
https://github.com/cuihantao/andes (or download and unzip it to the desired path).
Change the working directory to the root folder of andes and run

.. code:: bash

      python3 -m pip install -e .

Pip should take care of the rest.

Optional: Install `cvxoptklu` to use KLU for speed up.
`cvxoptklu` is a standalone KLU direct solver for linear equations.
KLU is generally ~20% faster than UMFPACK.
cvxoptklu requires a C compiler, and the `openblas` and
`SuiteSparse` libraries. ::

      python3 -m install cvxoptklu

Trouble-shooting
================
There is a known issue of CVXOPT with versions earlier than 1.2.2 in Windows.
If the time-domain simulation crashes for the `cases/ieee14/ieee14_syn.dm`,
please check and install the latest CVXOPT (=>1.2.2).
