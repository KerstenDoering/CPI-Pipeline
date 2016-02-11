#!/bin/python

from subprocess import Popen

def concat(infiles, outfile):
	# construct command
	cmd = ["cat"]
	cmd.extend(infiles)
	cmd.extend([">", outfile])

	# execute
	cmd = " ".join(cmd)
	print "Executing: `" + cmd +"`"
	job = Popen(cmd,shell=True)
	if job.returncode != None:
		raise RuntimeError # premature process termination

	return job

	
