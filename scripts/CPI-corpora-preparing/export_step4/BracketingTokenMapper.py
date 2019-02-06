#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Ammar -2019

import subprocess
import os
import time
from multiprocessing import Pool
from functools import partial
from optparse import OptionParser
import os.path

# This function to perform the bracketing tocken mapper
def _mapper(corpus, _file):

    cmd = "java -jar step_4_BracketingTokenMapper.jar "+ corpus +"/"+ _file + " > DS.xml.inj1-bracketing-tokens.txt.log 2>&1"

    process = subprocess.call(cmd, shell=True)
    
# To run the parallel processing
def run(corpus, PROCESSES):

  
    if (len(PROCESSES) == 1):

        PROCESSES = PROCESSES.zfill(2)

    paths = []

    for root, dirs, files in os.walk(corpus):
        for filename in sorted(files):
        
            paths.append(filename)

    paths.sort()



    pool = Pool(processes=int(PROCESSES))

    #print "Initialized with ", PROCESSES, "processes"
        

    result = pool.map_async(partial(_mapper, corpus), paths[0:])
    res = result.get()

    
if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus")
    
    
    parser.add_option("-p", "--processes",
                      dest="PROCESSES", default=2,
                      help="How many processes should be used. (Default: 2)")
    (options, args) = parser.parse_args()
    
    
    try:
    
        run(options.corpus, options.PROCESSES)

    except:
        pass

