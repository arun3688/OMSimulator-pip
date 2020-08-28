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
import subprocess
import os, sys, sysconfig
import multiprocessing
import git, tempfile


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
      
      clonedir = os.path.join(tempfile.gettempdir(),"OMSimulator")

      #remove git directory if exists
      if os.path.isdir(clonedir):
        git.rmtree(clonedir)
     
      print("Cloning git repository in the following location : ", clonedir)
      git.Repo.clone_from('https://github.com/OpenModelica/OMSimulator', clonedir, recursive=True)
      print("Cloning Successful")
        
      #print(os.getcwd())
      currentdir = os.getcwd()
      os.chdir(clonedir)
       
      ## config and build OMSimulator 
      if (sysconfig.get_platform() == 'linux-x86_64' or sysconfig.get_platform() == 'mingw'):
        subprocess.call(['make', 'config-3rdParty'])
        subprocess.call(['make', 'config-OMSimulator'])
        subprocess.call(['make', 'OMSimulator', '-j'+str(multiprocessing.cpu_count())])
      else:
        visualStudioVersion = ["VS14-Win32", "VS14-Win64", "VS15-Win32", "VS15-Win64"] 
        print("Building windows libraries, The following versions of Visual Studio are supported:")
        print("1." , visualStudioVersion[0] , "-> Visual Studio 14 2015")
        print("2." , visualStudioVersion[1] , "-> Visual Studio 14 2015 Win64")
        print("3." , visualStudioVersion[2] , "-> Visual Studio 15 2017")
        print("4." , visualStudioVersion[3] , "-> Visual Studio 15 2017 Win64")
        print("5. None, Exit and install the above visual studio version and build again:")
         
        choice = int(input("Enter Your choice (press (1 or 2 or 5) ) :"))
           
        if (choice > 5):
          print("Invalid choice, choose a valid choice from (1 to 5)")
          os.chdir(currentdir)
          git.rmtree(clonedir)
          quit()
        elif(choice == 5):
          print("! Quitting the installation, Please install any of the above Visual Studio version and continue")
          os.chdir(currentdir)
          git.rmtree(clonedir)
          quit()
        else:
          subprocess.call(['configWinVS.bat', visualStudioVersion[choice-1]])
          subprocess.call(['buildWinVS.bat', visualStudioVersion[choice-1], '-j'+str(multiprocessing.cpu_count())])
      
      print("### Build OMSimulator successful ###")
      #print(os.getcwd())
      os.chdir(currentdir)

      # copy OMSimulator package to root directory
      if sysconfig.get_platform() == 'linux-x86_64':
        copy_tree(os.path.join(clonedir,"install/linux/lib/OMSimulator"), target_dir)
      elif sysconfig.get_platform() == 'mingw':
        copy_tree(os.path.join(clonedir,"install/mingw/lib/OMSimulator"), target_dir)
      else:
        copy_tree(os.path.join(clonedir,"install/win/lib/OMSimulator"), target_dir)
        
      ## remove the git directory after copying the files
      git.rmtree(clonedir)

    build_py.run(self)

setup(
      name='OMSimulator',
      version='2.0.1',
      description='OMSimulator-Python API Interface',
      author='Open Source Modelica Consortium (OSMC)',
      author_email='openmodelicadevelopers@ida.liu.se',
      license="BSD, OSMC-PL 1.2, GPL (user's choice)",
      url='http://openmodelica.org/',
      install_requires=['GitPython'],
      packages=['OMSimulator'],
      cmdclass={'build_py': my_build_py},
      zip_safe = False
      )
