#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

    This script downloads PubMed annotated abstracts in BioC XML format from PubTator. It wraps this command:
    curl -H "content-type:application/json" http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Disease/1000475,1006519,1010707/BioC/ > text_PubTator.xml
    The the type of annotation (here: Disease) can be easily exchanged for a given list of PubMed-IDs (as well as the BioC XML output format). The maximum number of PubMed-IDs to send to PubTator (tested) is 21. Unfortunately, articles without abstract are not processed, but there is the possibility to submit raw text.
    Parameters: http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/#curl
"""
import urllib2
import sys
# module that wraps command-line parameters and is able to pipe the output
import subprocess
# parse parameters given for this script
from optparse import OptionParser
from subprocess import STDOUT
import datetime, time 
import os.path

# read PubMed-IDs from file and return them as a comma-separated string
def read_pmids(infile):
    #open file with PubMed-IDs
    f = open(infile,"r")
    #save all IDs in a list
    pmid_list = []
    for line in f:
        pmid_list.append(line.strip())
    #close file
    f.close()

    return pmid_list

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="i", help='name of the input file containing all PubMed-IDs, separated by line breaks (default: pmid_list.txt)', default="pmid_list.txt")
    parser.add_option("-o", "--outfile", dest="o", help='name of the output file containing all annotated abstracts in PubTator format from PubTator (default: text_PubTator.txt)', default="text_PubTator.txt")
    parser.add_option("-l", "--logfile", dest="l", help='name of the logfile, e.g. text_PubTator.log (optional)')
    parser.add_option("-t", "--trigger", dest="t", help='name of the BioConcept, e.g.: Chemical, Disease, Gene, Mutation, or Species (default: BioConcept)', default="BioConcept")
    parser.add_option("-f", "--format", dest="f", help='name of the output format, e.g.: BioC, JSON, or PubTator (default: PubTator)', default="PubTator")
    (options, args) = parser.parse_args()
    
    # save parameters in an extra variable
    log = options.l
    outfile = options.o
    infile = options.i
    trigger = options.t
    output_format = options.f

    if not os.path.exists(infile):
        print "input file: ", infile ," does not exits"
        sys.exit()
    
    if os.path.exists(outfile):
        os.remove(outfile)
            
    # get PubMed-IDs from file
    pmids = read_pmids(infile)

    startTime = time.asctime()
    
    k=0
    size = 20
    suffix = infile.split('_')[-1]

    pmidFile = open(infile, "r")
    
    pmids = pmidFile.read().splitlines()
    
    if not os.path.exists('missed_pmids/'):
        os.makedirs('missed_pmids/')

    if not os.path.exists('done_pmids/'):
        os.makedirs('done_pmids/')
    
    
        
    miss_pmids_outfile = open("missed_pmids/missed_pmids_"+suffix,'w')
    done_pmids_outfile = open("done_pmids/done_pmids_"+suffix,'w')
    outputfile = open(outfile,"a")
    for i  in range(0, len(pmids), size):
        if (i+size) > len(pmids):
            currnet_pmids = ",".join(pmids[i:])
            
        else:
            currnet_pmids = ",".join(pmids[i:i+size])

        
        try:
            url_Submit = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + trigger + "/" + currnet_pmids + "/" + output_format + "/"
            urllib_result = urllib2.urlopen(url_Submit)
            k=k+1
            outputfile.write(urllib_result.read())
            done_pmids_outfile.write(currnet_pmids)
            done_pmids_outfile.write('\n')
            if (i % 1000==0):
            
                print >> sys.stderr, "\rProcessing document " + suffix + " : " + str(i)
            
        except:
            miss_pmids_outfile.write(currnet_pmids)
            miss_pmids_outfile.write('\n')
            time.sleep( 10 )
        continue
        
    miss_pmids_outfile.close()
    done_pmids_outfile.close()
    outputfile.close()
    
    endTime = time.asctime()

