#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Kersten Doering 11.02.2015

# this script reads identifiers from DS1.xml-ptb-s.txt and adds them to DS1.xml-ptb-s.txt-parsed.txt with tab separation
# otherwise the programme of step 3 in the PPI preprocessing pipeline will not recognize the input sentences from Charniak-Johnson parser (step 2)

# get tags
tags = []
infile_tags = open("DS2.xml-ptb-s.txt","r")
for line in infile_tags:
    # a line looks like this:
    # <s DS1.d0.s0> Bestrophin-1  enables Ca2+-activated Cl-conductance in epithelia. </s>
    # whitespace splitting and removing of closing tag of the text element
    tag = line.strip().split(" ")[1][:-1]
    tags.append(tag)
infile_tags.close()

# add tags to sentences in Charniak-Johnson format (order is the same)
infile_parsed = open("DS2.xml-ptb-s.txt-parsed.txt","r")
# save modified version
outfile = open("DS2.xml-ptb-s.txt-parsed_modified.txt","w")
for index,line in enumerate(infile_parsed):
    outfile.write(tags[index]+"\t"+line)
infile_parsed.close()
outfile.close()
