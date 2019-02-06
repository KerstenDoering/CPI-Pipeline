#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import subprocess
import os
import time
from multiprocessing import Pool
from functools import partial
from optparse import OptionParser
import os.path
import shutil
from shutil import copyfile

currentPath=os.path.dirname(__file__)+"/"

# This function to perform the parsing process to build a syntactic tree
def _parseIt(corpus, _file):

    # perfom the parsing process to build a syntactic tree   
    cmd = "python " + currentPath + "parse.py -i " + currentPath + corpus +"/"+ _file + " -o "+ currentPath + corpus + "/"+ _file + "-parsed.txt"
    process = subprocess.call(cmd, shell=True)
    
# This function to split the input file to an equal segments, then parsing all those segments in parallel, finally concatenate all the intermediate outputs into one file with maintain the order of those outputs(e.g. segmet00-parsed.txt must be before segment01-parsed.txt and so on)
def run(_in_file, corpus, PROCESSES):

  
    if (len(PROCESSES) == 1):

        PROCESSES = PROCESSES.zfill(2)


    tmp = subprocess.check_output(['wc', '-l', _in_file])

    num = int(tmp.split()[0])/int(PROCESSES)

    splitDir = str(currentPath +corpus)

    if os.path.exists(splitDir):
        shutil.rmtree(splitDir)
    os.makedirs(splitDir)

    # Split the input file into an equal segments to process all of them in parallel.
    cmd = "split -d -l "+ str(num)+ " " + _in_file + " "+ currentPath +corpus +"/segment"
    process = subprocess.call(cmd, shell=True)

    # since the last seg. is almost very small, we can concatente it with the one before the last (e.g. segment08 to segment07)
    fileLastToRemove =  currentPath + corpus +"/segment"+ PROCESSES
    if os.path.exists(fileLastToRemove):
        cmd = "cat " + fileLastToRemove +" >> "+ currentPath + corpus+"/segment" + str(int(PROCESSES)-1).zfill(2)
        process = subprocess.call(cmd, shell=True)
        os.remove(fileLastToRemove)
    
    paths = []

    for root, dirs, files in os.walk(str(currentPath+corpus)):
        for filename in sorted(files):
        
            paths.append(filename)

    paths.sort()

    pool = Pool(processes=int(PROCESSES))

    result = pool.map_async(partial(_parseIt, corpus), paths[0:])
    res = result.get()


    # Concatenate the intermediate output (output from all the processors) into one output file
    fileToRemove = currentPath+corpus+".xml-ptb-s.txt-parsed.txt"
    try:
        os.remove(fileToRemove)
    except OSError:
        pass
    
    for i in range (0, int(PROCESSES)):

        cmd = "cat " + currentPath+ corpus + "/segment" + str(i).zfill(2) + "-parsed.txt" + " >> " + currentPath + corpus+".xml-ptb-s.txt-parsed.txt"

        process = subprocess.call(cmd, shell=True)

    src = currentPath + corpus+".xml-ptb-s.txt-parsed.txt"
    dest=os.getcwd()+"/Work/"
    shutil.move(src, dest)


if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-i", "--input", dest="input", 
                      default=None,
                      help="specify the path of the intput file")  
    parser.add_option("-c", "--corpus", dest="corpus",
                      default='DS',
                      help="specify the corpus")
    
    
    parser.add_option("-p", "--processes",
                      dest="PROCESSES", default=2,
                      help="How many processes should be used. (Default: 2)")
    (options, args) = parser.parse_args()
    
    
    try:
    
        run(options.input, options.corpus, options.PROCESSES)

    except:
        pass

