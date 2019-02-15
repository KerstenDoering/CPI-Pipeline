#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2018, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>
    This script To set or reflect the final prediction decision of the candidate interactions onto the input file .
"""

import sys, os
#import xml.etree.cElementTree as ElementTree
from lxml import etree as ElementTree

DictPrediction = {}

# This function to get all entities that are in the input file and store them in dictionary.
def getEntities(filename):

    tree = ElementTree.parse(filename)
    root = tree.getroot()
    sentences = root.getiterator("sentence")
    entityDict = {}
    pairDict = {}
    
    for sentence in sentences:
        print sentence.attrib["origId"]
        #entities = sentence.findall("entity")
        pairs = sentence.findall("pair")
        
        
        for pair in pairs:
            
            pairDict[pair.attrib["id"]] = pair
            

    print pairDict["DS1.d25.s1.i0"].attrib["e1"] , ":" , entityDict[pairDict["DS1.d25.s1.i0"].attrib["e1"]].attrib["text"]
    
    print pairDict["DS1.d25.s1.i0"].attrib["e2"] , ":" , entityDict[pairDict["DS1.d25.s1.i0"].attrib["e2"]].attrib["text"]
    #print entityDict["DS1.d25.s1.e1"].attrib["text"]


# This function to get all the final prediction decision that are in the output file(.sql) and store them in dictionary.
def getPrediction(filename):

    i = 0
    
    f = open(filename,'r')
    
    for line in f:
        if line[12:23] == "ppiCVoutput":
            segmnt = line.split(',')
            pairId = segmnt[4].strip()[1:-1]
            interaction = segmnt[5].strip()[1:-1]
            #print segmnt[4].strip(), ":", segmnt[5].strip()
            DictPrediction[pairId] = interaction
           
    f.close()

 
# This function to set or reflect the final prediction decision of the interaction onto the input file.
def setPairsInteraction(filename):

    tree = ElementTree.parse(filename)
    root = tree.getroot()
    sentences = root.getiterator("sentence")
    entityDict = {}
    pairDict = {}
    
    for sentence in sentences:
        #pair = ElementTree.Element("pair")
        
        pairs = sentence.findall("pair")
        
        for pair in pairs:
            pairId = pair.attrib["id"]
            #print "pairId :", pairId
            #interaction = DictPrediction[pairId]
            interaction = DictPrediction.get(pairId,None)
            #print "interaction : ", interaction
            #pair.set("interaction", interaction)
            
            if interaction == '1':
            
                pair.set("interaction", "True")
        
            elif interaction == '0':
                pair.set("interaction", "False")
            
            else:
                #pair.set("interaction", "Error")
                pair.set("interaction", "False") # Here the parser could not parse the sentence and this pair does not appear in the output, for that you can give assign False for this pair 
            
    return tree
 

if __name__ == "__main__":

    from optparse import OptionParser 
    
    parser = OptionParser()
    
    parser.add_option("-i", "--input", dest= "inputFileName")
    parser.add_option("-k", "--kernel", dest= "kernel")
    parser.add_option("-t", "--expTyp", dest= "expType")
    parser.add_option("-r", "--result", dest= "resultFileName")
    parser.add_option("-o", "--output", dest="outFileName")
    
    (options, args) = parser.parse_args()
    
    print "Set the final prediction decisions of the candidate interactions..."

    inputFile = 'generate_XML_files/DS/'+ options.inputFileName
    resultFile = 'ppi-benchmark/Experiments/' + options.kernel + os.sep + options.expType + os.sep + options.resultFileName
    outputFile = 'ppi-benchmark/Experiments/' + options.kernel + os.sep + options.expType + os.sep + options.outFileName
    
    getPrediction(resultFile)
    convertedCorpusTree =  setPairsInteraction(inputFile)
    convertedCorpusTree.write(outputFile)

