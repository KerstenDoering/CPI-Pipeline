#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Elham Abbasian <e_abbasian@yahoo.com>, Kersten Doering <kersten.doering@gmail.com>

    This script will be called by APG_pipeline_DS2.sh from scripts/CPI-corpora-preparing/splitting/ to rename the files from DS2<number>.txt to test-<number>.
"""

import os
import re
from glob import glob

# get file names from splitting directory
list_of_files = os.listdir("DS2")
# change to this directory
os.chdir("DS2")
# iterate over all files and change their names
for index,name in enumerate(list_of_files):
    old_name = name
    file_number_obj=re.match('DS2(\d+).txt',list_of_files[index])
    file_number = file_number_obj.group(1)
    new_name = "test-"+str(file_number)
    for filename in glob(old_name):
        os.rename(filename,new_name)
# change back to the parent directory
os.chdir("..")
