#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   Ammar Qaseem

import sys
import os
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from functools import partial
from optparse import OptionParser


def split_AllGraphTrans(corpus, filename):

    file_indx=filename.split("-")[3]

    d = {}
    with open(filename) as f:
        for line in f:
           (val, key) = line.split()
           d[key] = int(val)

    testFile_name = "CV/" + corpus + "/test" + str(int(file_indx)-1)+".txt"
    testFile = open(testFile_name,'w') ##
    testFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><corpus source=\""+corpus+"\">\n") ##

    trainFile_name = "CV/" + corpus + "/train" + str(int(file_indx)-1)+".txt"
    trainFile = open(trainFile_name,'w')
    trainFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><corpus source=\""+corpus+"\">\n") ##

    testFile.close()
    trainFile.close()

    _in_file= corpus + '.xml'
    context = ET.iterparse(_in_file, events=('end', ))
    index = -1
    for event, elem in context:
        if elem.tag == 'document':
        
            DocumentID = elem.attrib.get('id')

            index += 1
            sys.stdout.write("Documents progressed: %d\r" % index )
            sys.stdout.flush()
            
            if DocumentID in d:

                testFile = open(testFile_name,'a')

                testFile.write(ET.tostring(elem))
                
                del d[DocumentID]
                

            else:
            
                trainFile = open(trainFile_name,'a')
                
                trainFile.write(ET.tostring(elem))
                         
            elem.clear()

    trainFile.write("</corpus>")
    testFile.write("</corpus>")
    trainFile.close()
    testFile.close()
    sys.stdout.write("\n")


def run(corpus, folds):

    paths = []

    split_test_train_path = 'splits-test-train/' + corpus + '/'
    
    for root, dirs, files in os.walk(split_test_train_path):
        for filename in sorted(files):
            
            paths.append(os.path.join(root,filename))

    paths.sort()

    pool = Pool(processes=folds)    # start with processors
    print "Initialized with ", folds, "processes"

    result = pool.map_async(partial(split_AllGraphTrans, corpus), paths[0:folds])
    
    res = result.get()

    print "\n \n"

           

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus") 

    (options, args) = parser.parse_args()
    

    # We will run through all the 10 files(folds)
    #path = 'splits-test-train/' + options.corpus + '/'
    run(options.corpus, 10)
    ##run_xmlsplit(options.corpus)
