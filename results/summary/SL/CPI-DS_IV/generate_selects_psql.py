#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    The script uses two different corpora and all combinations for w,n in (1,3) x (1,3) to generate a shell script for the selection of all results from a PostgreSQL database.
"""

# write PostgreSQL selection commands to shell script
outfile = open("get_csv_results.sh","w")
# two corpora
corpora = ["CPI-DS_IV"]
# basic selection command
string = """psql -c "\copy (select corpus, c, tp, fn, tn, fp, total, auc, precision_, recall, f_measure from ppicv where kernel_script = 'jsre; n=%s (n-gram), w=%s (window)' and corpus = '%s') TO 'output/%s.csv' WITH CSV" -h localhost -d ppi -U ppi"""
# iterate over corpora
for corpus in corpora:
    # iterate over n 1,2,3
    for n in range(1,4):
        # iterate over w 1,2,3
        for w in range(1,4):
            # write down selection command
            outfile.write(string % (str(n), str(w), corpus, corpus + "_n_" + str(n) + "_w_" + str(w)) + "\n")
# close file
outfile.close()
