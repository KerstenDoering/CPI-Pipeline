#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Elham Abbasian <e_abbasian@yahoo.com>, Kersten Doering <kersten.doering@gmail.com>

    This script will be called by APG_pipeline_DS1.sh from scripts/CPI-corpora-preparing/splitting/ to rename the files from DS1<number>.txt to test-<number>.
"""

import os
import re
from glob import glob
from optparse import OptionParser

def rename_files(corpus):

    # get file names from splitting directory
    _in_file= corpus + '.xml.inj1'
    list_of_files = os.listdir(corpus)
    # change to this directory
    os.chdir(corpus)
    # iterate over all files and change their names
    for index,name in enumerate(list_of_files):
        old_name = name
        exp =  corpus + '(\d+).txt'
        file_number_obj=re.match(exp,list_of_files[index])
        if file_number_obj is  None: continue   ##
        file_number = file_number_obj.group(1)
        new_name = "test-"+str(file_number)
        for filename in glob(old_name):
            os.rename(filename,new_name)
    # change back to the parent directory
    os.chdir("..")
    
    print "renaming the files has been done...\n"    

if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus") 

    (options, args) = parser.parse_args()

    rename_files(options.corpus)
