#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = """
This file is part of OpenModelica.
Copyright (c) 1998-CurrentYear, Open Source Modelica Consortium (OSMC),
c/o Linköpings universitet, Department of Computer and Information Science,
SE-58183 Linköping, Sweden.
All rights reserved.
THIS PROGRAM IS PROVIDED UNDER THE TERMS OF GPL VERSION 3 LICENSE OR
THIS OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
ACCORDING TO RECIPIENTS CHOICE.
The OpenModelica software and the Open Source Modelica
Consortium (OSMC) Public License (OSMC-PL) are obtained
from OSMC, either from the above address,
from the URLs: http://www.ida.liu.se/projects/OpenModelica or
http://www.openmodelica.org, and in the OpenModelica distribution.
GNU version 3 is obtained from: http://www.gnu.org/copyleft/gpl.html.
This program is distributed WITHOUT ANY WARRANTY; without
even the implied warranty of  MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE, EXCEPT AS EXPRESSLY SET FORTH
IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE CONDITIONS OF OSMC-PL.
See the full OSMC Public License conditions for more details.
"""
__author__ = "Open Source Modelica Consortium (OSMC)"
__maintainer__ = "https://openmodelica.org"
__status__ = "Production"


from setuptools import setup
from distutils.command.build_py import build_py
from distutils.file_util import copy_file
from distutils.dir_util import copy_tree
import os, sysconfig
import tempfile
import requests, zipfile, io, shutil


topdir= os.path.join(os.getcwd(), 'OMSimulator')
## check if directory exist and remove 
if os.path.isdir(topdir):
  os.rmdir(topdir)

## create a dummy directory, so that setuptools creates the package directory
os.mkdir(topdir)

## overrride build_py, for compiling and copying the dlls
class my_build_py(build_py):
  def run(self):
    if not self.dry_run:
      target_dir = os.path.join(self.build_lib, 'OMSimulator')
      
      # mkpath is a distutils helper to create directories
      self.mkpath(target_dir)
      
      ## download the zip directory from url 
      if (sysconfig.get_platform() == 'linux-x86_64'):
        r = requests.get("https://test.openmodelica.org/jenkins/job/OMSimulator/job/master/lastSuccessfulBuild/artifact/OMSimulator-linux-amd64*/*zip*/archive.zip")
      elif (sysconfig.get_platform() == 'mingw'):
        r = requests.get("https://test.openmodelica.org/jenkins/job/OMSimulator/job/master/lastSuccessfulBuild/artifact/OMSimulator-mingw64*/*zip*/archive.zip")
      elif (sysconfig.get_platform() == "win-amd64"):
        r = requests.get("https://test.openmodelica.org/jenkins/job/OMSimulator/job/master/lastSuccessfulBuild/artifact/OMSimulator-win64*/*zip*/archive.zip")

      z = zipfile.ZipFile(io.BytesIO(r.content))
      
      zipInfo = z.namelist()[0]
      dirname, extension = os.path.splitext(zipInfo)

      tempDir = tempfile.gettempdir()
      zipFilePath = os.path.join(tempDir, zipInfo)
      
      if os.path.exists(zipFilePath):
        os.remove(zipFilePath)

      ## copy the zip file in temp directory
      z.extractall(tempDir)
      z.close()

      zipDir = os.path.join(tempDir, dirname)
      #remove zip directory if exists
      if os.path.isdir(zipDir):
        shutil.rmtree(zipDir)

      ## unzip the zip file
      shutil.unpack_archive(zipFilePath, zipDir)

      # copy OMSimulator package to root directory
      copy_tree(os.path.join(zipDir,"lib/OMSimulator"), target_dir)

      ## remove the zip directory after copying the files
      shutil.rmtree(zipDir)
      ## remove the zip file
      os.remove(zipFilePath)
      print("### Build OMSimulator successful ###")

    build_py.run(self)

setup(
      name="OMSimulator",
      version="latest",
      description="OMSimulator-Python API Interface",
      author="Open Source Modelica Consortium (OSMC)",
      author_email="openmodelicadevelopers@ida.liu.se",
      license="BSD, OSMC-PL 1.2, GPL (user's choice)",
      url="http://openmodelica.org/",
      install_requires=["requests"],
      packages=["OMSimulator"],
      cmdclass={'build_py': my_build_py},
      zip_safe = False
      )
