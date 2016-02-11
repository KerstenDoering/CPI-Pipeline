#!/bin/python

import os
import glob
import subprocess
import re
import time

def runDistributed(numberOfJobs, commands):
    numberOfJobs = min(numberOfJobs, len(commands))
    jobs=[None]*numberOfJobs #Active Jobs List
    
    #Start as many jobs as cpus
    for i in range(numberOfJobs):
        current=commands.pop(0)
        print "Executing: `" + current +"`"
        jobs[i]=subprocess.Popen(current,shell=True)#, stderr=subprocess.PIPE

    #Are there any jobs left in the set commands?
    while(len(commands)>0):
        time.sleep(1)  #Poll every 1

        for i in range(numberOfJobs):
            if(jobs[i].poll()!=None):#Job[i] is finished? 
#                print jobs[i].stderr.readline().rstrip() 
                
                if(len(commands)==0): #Are there unstarted jobs left?
                    break
                else:
                    current=commands.pop(0)
                    print "Executing: `" + current +"`"
                    jobs[i]=subprocess.Popen(current,shell=True)

    #let the jobs complete
    while True:
        finished=True
        for i in range(numberOfJobs):
            if(jobs[i].poll()==None):
                finished=False

        if(finished):
            return(0)
        time.sleep( 1 )
