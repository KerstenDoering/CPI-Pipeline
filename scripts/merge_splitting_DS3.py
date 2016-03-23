#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    This script reads all concatenated cross-validation files from DS1 and DS2 in /home/kersten/Desktop/CPI-Pipeline/scripts/splitting/DS3/. It also parses all PubMed ID-DS3 identifiers in CPI-Pipeline/scripts/CPI-corpora-preparing/splitting/DS3/. The new files will contain the cross-validation parts from the DS1 and DS2 experiments with the new identifiers from DS3.
"""

# change paths
import os

# store name-PubMed ID pairs in a dictionary
name_pmid = {}
# get concatenated file names
concatenated_files = os.listdir("splitting/DS3")
# change to this directory
os.chdir("splitting/DS3")
# iterate over all files and store the PubMed IDs for each file name
for name in concatenated_files:
    # use file name as key and list of PubMed IDs as value
    name_pmid[name] = []
    # open input file
    infile = open(name,"r")
    # read all PubMed IDs and store them in the dictionary
    for line in infile:
        pmid = line.split(" ")[0]
        name_pmid[name].append(pmid)
    # close file
    infile.close()

# change back into the starting directory
os.chdir("../..")
# get all file names
new_files = os.listdir("CPI-corpora-preparing/splitting/DS3")
# change into the new DS3 cross-validation directory
os.chdir("CPI-corpora-preparing/splitting/DS3")
# iterate over all files and store all PubMed ID-identifier pairs in a dictionary
pmid_identifier = {}
for name in new_files:
    infile = open(name,"r")
    # start parsing
    for line in infile:
        # temp[0] contains the PubMed ID. temp[1] is the identifier
        temp = line.strip().split(" ")
        pmid_identifier[temp[0]] = temp[1]
    # close file
    infile.close()

# iterate again over all file names (the new files are already renamed from DS31.txt to test-1) and merge PubMed IDs and identifiers referring to the order of DS1 and DS2
for name in concatenated_files:
    outfile = open(name,"w")
    for pmid in name_pmid[name]:
        outfile.write(pmid + " " + pmid_identifier[pmid] + "\n")
    outfile.close()

# change back into the directory from which the pipeline continues to copy the preprocessed files before starting the experiment
os.chdir("..")
