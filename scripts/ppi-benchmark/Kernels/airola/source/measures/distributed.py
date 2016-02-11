#!/bin/python

import os
import sys
import glob
import subprocess
import re
import time

def runDistributed(numberOfJobs, commands):
    if not commands:
        raise ValueError #empty list
	# limit the number of jobs to the number of tasks
    if len(commands) < numberOfJobs:
        numberOfJobs=len(commands)

    jobs=[None]*numberOfJobs #Active Jobs List
    cmds=[None]*numberOfJobs #Active Command List
    
    #Start as many jobs as cpus
    for i in range(numberOfJobs):
        current=commands.pop(0)
        cmds[i]=current
        jobs[i]=subprocess.Popen(cmds[i],shell=True)#, stderr=subprocess.PIPE)

    #Are there any jobs left in the set commands?
    while(len(commands)>0):
        time.sleep(10)  #Poll every 10 sec

        for i in range(numberOfJobs):
            if(jobs[i].poll()!=None):#Job[i] is finished? 
            	if jobs[i].returncode != 0:
                    print >> sys.stderr, "job failed (ERRNO: %d):\n%s" %(jobs[i].returncode, cmds[i])
                    raise RuntimeError # job returned non-zero exitcode
#                print jobs[i].stderr.readline().rstrip() 
                
                if(len(commands)==0): #Are there unstarted jobs left?
                    break
                else:
                    current=commands.pop(0)
                    cmds[i]=current
                    jobs[i]=subprocess.Popen(cmds[i],shell=True)#,stderr=subprocess.PIPE)

    #let the jobs complete
    while True:
        finished=True
        for i in range(numberOfJobs):
            if(jobs[i].poll()==None):
                finished=False
            elif jobs[i].returncode != 0:
                print >> sys.stderr, "job failed (ERRNO: %d):\n%s" %(jobs[i].returncode, cmds[i])
                raise RumtimeException # job returned non-zero exitcode
            
				

        if(finished):
            return(0)
        time.sleep( 10 )
	
