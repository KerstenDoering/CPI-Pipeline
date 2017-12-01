#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Ammar Qaseem

import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser


def run_xmlsplit(corpus):
    _in_file= corpus + '.xml.inj1'
    
    #context = ET.iterparse('DS1.xml.inj1', events=('end', ))
    context = ET.iterparse(_in_file, events=('end', ))
    
    index = -1
    for event, elem in context:
        
        if elem.tag == 'document':
            index += 1
            sys.stdout.write("Documents progressed: %d\r" % index )
            sys.stdout.flush()
            
            _out_file = format(corpus + "/" + str(index) + ".xml")
            with open(_out_file, 'wb') as f:
                f.write("<corpus source=\""+corpus+"\">\n")
                f.write(ET.tostring(elem))
                f.write("</corpus>")
                
            f.close()
            elem.clear()    
        
                
    sys.stdout.write("\n")

if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus") 

    (options, args) = parser.parse_args()

    run_xmlsplit(options.corpus)
