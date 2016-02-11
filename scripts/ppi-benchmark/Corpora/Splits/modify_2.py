#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    This script removes the PubMed ID in front of the document ID for each instance in the text files. 
"""

import os

# get current directory
mypath = os.getcwd()
# change into data set directory and get file names
os.chdir("DS2")
files = os.listdir(os.getcwd())
# start iteration and get all document IDs (space-separated format)
for infile in files:
    f = open(infile,"r")
    identifier = []
    for line in f:
        identifier.append(line.strip().split(" ")[1])
    f.close()
    # overwrite each file with the new format (wihtout PubMed ID)
    f = open(infile,"w")
    for elem in identifier:
        f.write(elem + "\n")
    f.close()
