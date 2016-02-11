#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2014, Kersten Doering <kersten.doering@gmail.com>

    This parser reads the HTML document Relationship_Mining.html.
    The algorithm extracts its sentences based on the status Interaction or 
    No Interaction. The sentences with the status False Positive are excluded.
"""

# module to make use of regular expressions
import re

# input file (HTML document)
infile = open("Relationship_Mining.html","r")
# two output files
outfile_interactions = open("interactions.txt","w")
outfile_no_interactions = open("no_interactions.txt","w")
# two debug files to check what was extracted from the HTML document
outfile_pmids = open("pmids_index.csv","w")
outfile_fp = open("pmids_fp.csv","w")
# initialize variables
# HTML document index of the considered sentence
index = 0
# PubMed ID of the considered sentence
pmid = 0
# sentence variable
sentence = ""
# status of the sentence
relation =""
# flag variables to determine the (repeating) fragment the parser is reading
# index read
in_index = False
# PubMed ID read
in_pmid = False
# sentence read
in_sentence = False
# <td> (table element) read
td_start = False
# string supporting the identification of a row showing a sentence index
numbers = "0123456789"
# debug number of sentences with status False Positive
counter_FP = 0
# debug number of sentences with status Interaction
counter_interaction = 0
# debug number of sentences with status No Interaction
counter_no_interaction = 0
# iterate over lines in HTML document
for line in infile:
    # skip empty lines
    if not line.strip() == "":
        # if the line starts with a number and the index is already set to True, set the pmid flag to True, too
        if in_index and line.strip()[0] in numbers and not in_pmid:
            # read PubMed ID
            pmid = line.strip()
            in_pmid = True
        # if the line starts with a number and the index flag is not yet set to True, set the index flag to True
        # if the index flag is set to True, the next number will be the PubMed ID
        # as there are some pmids with more than one sentence, this index flag is important to reconstruct the exact example (open and close table element with <td> and </td>
        if line.strip()[0] in numbers and not in_index:
            index = line.strip()
            in_index = True
        # if PubMed ID and index flag are to True, the line with the sentence can be recognised by the colour tag (e.g. "background-color:light")
        # a sentence can only be read after a <td> element was read (td_start set to True)
        if in_pmid and in_index and td_start and "</td>" in line:
            td_start = False
            in_sentence = True
            sentence = sentence.strip()
        if in_pmid and in_index and td_start:
            sentence += " " + line.strip()
        if in_pmid and in_index and "<td>" in line:
            td_start = True
        # this regular expression refers to the special line structure showing the status of a sentence
        if in_pmid and in_index and in_sentence and line.strip().startswith("<td id=\"box"):
            relation = re.match("<td id=\"box[0-9]*?\">(.*?)</td>",line.strip()).group(1)
            # the next two if clauses here are actually a bit redundant (ToDo change)
            # the only difference is the counter for "interaction" or "no_interaction"
            # store the sentence in the output file and set the index, PubMed ID, and sentence flag to False, again
            if relation == "Interaction":
                outfile_interactions.write(pmid+"-"+index+"\t"+sentence+"\n")
                in_index = in_pmid = in_sentence = False
                sentence = relation = ""
                counter_interaction += 1
                outfile_pmids.write(pmid+"\t"+index+"\n")
            if relation == "No Interaction":
                outfile_no_interactions.write(pmid+"-"+index+"\t"+sentence+"\n")
                in_index = in_pmid = in_sentence = False
                sentence = relation = ""
                counter_no_interaction += 1
                outfile_pmids.write(pmid+"\t"+index+"\n")
            # debug: count sentences with status False Positive
            if relation == "False positive example":
                in_index = in_pmid = in_sentence = False
                sentence = relation = ""
                counter_FP += 1
                outfile_fp.write(pmid+"\t"+index+"\n")

# close files
infile.close()
outfile_interactions.close()
outfile_no_interactions.close()
outfile_pmids.close()
outfile_fp.close()
# debug output what was counted
print "FP:"
print counter_FP
print "interactions:"
print counter_interaction
print "no interactions:"
print counter_no_interaction
print "total:"
total = counter_FP + counter_interaction + counter_no_interaction
print total

