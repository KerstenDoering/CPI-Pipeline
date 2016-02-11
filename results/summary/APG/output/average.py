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
keys = ["c","recall","specificity","precision","accuracy","f1_score","auc"]#,"calculated_f1_score"
# iterate over files
for name in files:
    # result files from data set 1
    if name.endswith(".csv") and "DS1" in name:
        # dictionary initialization with all parameters
        DS1 = {"c":0.0,"auc":0.0,"precision":0.0,"accuracy":0.0,"recall":0.0,"f1_score":0.0,"specificity":0.0,"calculated_f1_score":0.0}
        infile = open(name,"r")
        # get all values and calculate rest of the parameters
        for line in infile:
            temp = line.strip().split(",")
            c = float(temp[1])
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
            DS1["c"] += c
            DS1["auc"] += auc
            DS1["precision"] += precision
            DS1["recall"] += recall
            DS1["f1_score"] += f1_score
            DS1["specificity"] += specificity
            DS1["accuracy"] += accuracy
            DS1["calculated_f1_score"] += calculated_f1_score
        infile.close()
        new_name = name.replace(".csv", "average.csv")
        # write results to file, build average and round with one decimal place
        outfile = open(new_name,"w")
        string = ""
        for key in keys:
            if not key == "c":
                string += str('%.1f' % round((DS1[key]/10.)*100.,1))+"\t"
            # parameter 'c' with two decimal places
            else:
                string += str('%.2f' % round(DS1[key]/10.,2))+"\t"
        string = string.strip()
        string += "\n"
        outfile.write(string)
        outfile.close()
    # the same procedure for data set 2
    elif name.endswith(".csv") and "DS2" in name:
        # dictionary initialization with all parameters
        DS2 = {"c":0.0,"auc":0.0,"precision":0.0,"accuracy":0.0,"recall":0.0,"f1_score":0.0,"specificity":0.0,"calculated_f1_score":0.0}
        infile = open(name,"r")
        # get all values and calculate rest of the parameters
        for line in infile:
            temp = line.strip().split(",")
            c = float(temp[1])
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
            DS2["c"] += c
            DS2["auc"] += auc
            DS2["precision"] += precision
            DS2["recall"] += recall
            DS2["f1_score"] += f1_score
            DS2["specificity"] += specificity
            DS2["accuracy"] += accuracy
            DS2["calculated_f1_score"] += calculated_f1_score
        infile.close()
        # write results to file, build average and round with one decimal place
        new_name = name.replace(".csv", "average.csv")
        outfile = open(new_name,"w")
        string = ""
        for key in keys:
            if not key == "c":
                string += str('%.1f' % round((DS2[key]/10.)*100.,1))+"\t"
            else:
                string += str('%.2f' % round(DS2[key]/10.,2))+"\t"
        string = string.strip()
        string += "\n"
        outfile.write(string)
        outfile.close()

