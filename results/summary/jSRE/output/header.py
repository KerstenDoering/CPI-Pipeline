#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    The script adds parameter headers to the concatenated files:
        python average.py
        cat DS1*average.csv > DS1_average.csv
        cat DS2*average.csv > DS2_average.csv
        python header.py
"""
# headers
keys = ["n","w","Sensitivity","Specificity","Precision","Accuracy","F1-score","AUC"]
# read file and write input to the new ouput file
infile = open("DS1_average.csv","r")
outfile = open("DS1_average_header.csv","w")
outfile.write("\t".join(keys) + "\n")
for line in infile:
    # also possible with a comma character
    outfile.write(line)#.replace(".",",")
infile.close()
outfile.close()
# read file and write input to the new ouput file
infile = open("DS2_average.csv","r")
outfile = open("DS2_average_header.csv","w")
outfile.write("\t".join(keys) + "\n")
for line in infile:
#    # also possible with a comma character
    outfile.write(line)#.replace(".",",")
infile.close()
outfile.close()

