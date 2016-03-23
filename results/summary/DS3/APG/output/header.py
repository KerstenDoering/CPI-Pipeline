#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    The script adds parameter headers to the concatenated files:
        python average.py
        cat DS3*average.csv > DS3_average.csv
        python header.py
"""
# headers
keys = ["Parameter","Sensitivity","Specificity","Precision","Accuracy","F1-score","AUC"]
# read file and write input to the new ouput file
infile = open("DS3_average.csv","r")
outfile = open("DS3_average_header.csv","w")
outfile.write("\t".join(keys) + "\n")
for line in infile:
    # also possible with a comma character
    outfile.write(line)#.replace(".",",")
infile.close()
outfile.close()
