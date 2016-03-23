#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Elham Abbasian <e_abbasian@yahoo.com>, Kersten Doering <kersten.doering@gmail.com>

    This script will be called by SL_pipeline_DS3.sh to rename the all-paths graph kernel cross-validation files from test-<number> to DS3<number>.txt. 
"""

import os
import re
from glob import glob

# get file names from splitting directory
list_of_files = os.listdir("DS3")
# change to this directory
os.chdir("DS3")
# iterate over all files and change their names
for index,name in enumerate(list_of_files):
    old_name = name
    file_number_obj=re.match('test-(\d+)',list_of_files[index])
    file_number = file_number_obj.group(1)
    new_name = "DS3"+str(file_number)+".txt"
    for filename in glob(old_name):
        os.rename(filename,new_name)
# change back to the parent directory
os.chdir("..")
