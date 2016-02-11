#/bin/python

import sys

def addids(file, idfile):

    f = open(file)
    g = open(idfile)
    array= []
    for line in f:
        line = line.rstrip().split()
	id = g.readline().split()[1]
	#print "id: " + id
	line[0] = id
        array.append(" ".join(line))
    f.close()
   
    # overwrite
    f = open(file, 'w')
    while(len(array)>0):
        f.write(array.pop(0) +"\n")

