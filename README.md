# OMSimulator-pip [![License: OSMC-PL](https://img.shields.io/badge/license-OSMC--PL-lightgrey.svg)](OSMC-License.txt)

The OMSimulator-pip project provides a pip setup for OMSimulator.

Installation
============
1) Installation using ``pip`` is recommended
    ```
    pip3 install OMSimulator (or)
    pip install OMSimulator
    ```
    
2) Installation from source can be done through cloning the repository and running the following commands
    ```
    cd <OMSimulator-pip>
    python setup.py install
    ```

Usage
=====
Running the following commands should get you started

```
  from OMSimulator import OMSimulator
  oms = OMSimulator()
  oms.version
```

Documentation
=============
The latest documentation is avilable as [html](https://www.openmodelica.org/doc/OpenModelicaUsersGuide/latest/omsimulator.html#omsimulatorpython)


Uploading the package to PyPi
=============================
1) Create an account at https://pypi.org/
2) Use twine to upload the distribution packages, twine can be installed via pip
    ```
     pip install twine
    ```
3) Generate source distribution archive of the package, this can be done by running the following command
    ```
     cd <OMSimulator-pip>
     python setup.py sdist
    ```
    The above command should output a "dist" directory which contains a "tar.gz" file which is the source archive
4) Finally upload the package using twine
    ```
     twine upload dist/*
    ```
