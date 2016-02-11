from PerformanceMeasures import computeAUC
import math
import sys

def readResults(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc

if __name__=="__main__":
    if len(sys.argv)!=2:
        print "Usage: python ComputeAuc RESULTFILE"
        sys.exit(0)
    else:
        f = open(sys.argv[1])
        auc = readResults(f)
        f.close()
        print "AUC: %f" %(auc)
