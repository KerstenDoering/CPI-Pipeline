#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    The script reads all result files from get_csv_results.sh and calculates the evaluation parameter averages of the 10 cross-validation folds.
"""

# file and path operations
import os
# get current directory
mypath = os.getcwd()
# get files in this directory
files = os.listdir(mypath)
# debug:
# print files
# evaluation parameters
keys = ["n","w","recall","specificity","precision","accuracy","f1_score","auc"]#,"calculated_f1_score"]
# iterate over files
for name in files:
    new_name = name.replace(".csv", "average.csv")
    # result files from data set 1
    if name.endswith(".csv") and "CPI-DS_IV" in name:
        # get parameters
        params = name.split("_")
        n = params[3]
        #print params[5]
        w = params[5].split(".")[0]
        # dictionary initialization with all parameters
        DS1 = {"w":w,"n":n,"auc":0.0,"precision":0.0,"accuracy":0.0,"recall":0.0,"f1_score":0.0,"specificity":0.0,"calculated_f1_score":0.0}
        infile = open(name,"r")
        # get all values and calculate rest of the parameters
        for line in infile:
            temp = line.strip().split(",")
            auc = float(temp[7])
            precision = float(temp[8])
            recall = float(temp[9])
            f1_score = float(temp[10])
            # specificity = TN/(TN+FP), TN = temp[4], FP = temp[5]
            specificity = float(temp[4])/(float(temp[4])+float(temp[5]))
            # accuracy = (TN+TP)/total
            accuracy = (float(temp[4]) + float(temp[2]))/float(temp[6])
            # f1_score = 2 * precision * recall/ (precision +recall)
            calculated_f1_score = 2 * precision * recall / (precision + recall)
            DS1["w"] = w
            DS1["n"] = n
            DS1["auc"] += auc
            DS1["precision"] += precision
            DS1["recall"] += recall
            DS1["f1_score"] += f1_score
            DS1["specificity"] += specificity
            DS1["accuracy"] += accuracy
            DS1["calculated_f1_score"] += calculated_f1_score
        infile.close()
        # write results to file, build average and round with one decimal place
        outfile = open(new_name,"w")
        string = ""
        for key in keys:
            if not key == "w" and not key == "n":
                string += str('%.1f' % round((DS1[key]/10.)*100.,1))+"\t"
            else:
                string += DS1[key]+"\t"
        string = string.strip()
        string += "\n"
        outfile.write(string)
        outfile.close()
