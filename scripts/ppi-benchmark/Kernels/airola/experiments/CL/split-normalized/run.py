#!/usr/bin/python
#nice python run.py 1>run.out 2>run.err
import os
import glob
import subprocess
import re
import time
import math
import sys

source='/vol/home-vol3/wbi/thomas/workspace/Kernels/airola/source'
sys.path.append(source +'/measures/')
base="/vol/home-vol3/wbi/thomas/workspace/Kernels/airola/experiments/CL/split-normalized/"


from distributed import *
from PerformanceMeasures import computeAUC
from Fscore import *
from Utilities import optimalFThreshold


def readAUC(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc



tokenizer="split"
parser="split_parse"

splits="corpus" 
dictionary="dictionary" #subfolder contains all dictionaries
linearized="linearized" #Subfolder containing the linearized features
normalized="normalized" #Subfolder containing the normalized linearized features
trained="trained"       #Subfolder containing the trained 
predict="predict"       #Subfolder containing the predicted values

run=normalized

corpora= os.listdir(base+splits) #Contains all five corpora
"""
#First Step; generate a dictionary for each train[0-9].txt
print "Step1: Generating Dictionary"
cmd =[]
for corpus in corpora:
    print corpus
    os.makedirs(base +dictionary +os.sep +corpus)
    train = base+splits +os.sep +corpus +os.sep +"train.xml.gz"
    cmd.append("python " +source +os.sep + "BuildDictionaryMapping.py -p " +parser +" -t " +tokenizer +" -i " +train  +" -o " +base +dictionary +os.sep +corpus  +".xml.gz")
runDistributed(5, cmd)

#Step Two: Generate 
#compute the graph kernels for your data, producing a linearized feature representation corresponding to the graph kernels.
print "Step2: Generating linearized feature representation"
cmd =[]
for corpus in corpora:
    print corpus
    os.makedirs(base +linearized +os.sep +corpus)
    for data in glob.glob(base+splits +os.sep +corpus +os.sep +"*.gz"): #Get train and test data
        cmd.append( "python " +source +os.sep + "LinearizeAnalysis.py -p " +parser +" -t " +tokenizer  +" -i " +data +" -d " +base +dictionary +os.sep +corpus +".xml.gz" +" -o " +base+linearized+os.sep +corpus+os.sep+os.path.basename(data))
runDistributed(4, cmd) 



#Step Three: you can normalize the data vectors to unit length. Sometimes this can boost the results, sometimes it makes them worse.
print "Step3:Normalize data"
cmd= []
for corpus in corpora:
    print corpus
    os.makedirs(base +normalized +os.sep +corpus)
    for data in glob.glob(base +linearized +os.sep +corpus +os.sep +"*.gz"): #Iterate over all Splits
        cmd.append("python " +source +os.sep + "NormalizeData.py -i" +data +" -o " +base + normalized +os.sep +corpus +os.sep + os.path.basename(data))
runDistributed(8, cmd)        


#Step4: Train a  model for each trainingset
print "Step4: Train a model for each Trainingset"
regex = re.compile('\D+\d+')  
cmd=[] #Put all commands in a 
for corpus in corpora: #Iterate over corpora
    print corpus
    train = base +run +os.sep +corpus +os.sep +"train.xml.gz"
    trainName= os.path.basename(train)
    
    dir= base +trained +os.sep +corpus +os.sep
    os.makedirs(dir)

    for l in range(-2,2): #Gridsearch
        lamda= pow(2,l) 
        cmd.append("python " +source +os.sep +"TrainLinearized.py -b 2000 -r " +str(lamda) +" -i " +train +" -o "  +dir + "train" +str(lamda) +".model")

runDistributed(4, cmd)


#print "Step 5 predict!"
cmd= []
regex = re.compile('(train)(\d+\.?\d*)(\.model)')
for corpus in corpora:
    print corpus
    eval=  base + run +os.sep +corpus +os.sep +"test.xml.gz" #Evaluation corpus
    train= base + run +os.sep +corpus +os.sep +"train.xml.gz" #Training corpus; needed for parameter selection

    outdir= base +predict +os.sep +corpus  +os.sep
    os.makedirs(outdir)   


    for trainModel in glob.glob(base +trained +os.sep +corpus +os.sep +"*"):
        model = trainModel
        lamda = regex.search(os.path.basename(model)).group(2)
        cmd.append("\npython " +source +os.sep +"TestLinearized.py -i " +eval  +" -m " +model  +" -o "  +outdir +"predict" +lamda  +".out")
        cmd.append("python " +source +os.sep +"TestLinearized.py -i " +train  +" -m " +model  +" -o "  +outdir +"threshold" +lamda  +".out")

runDistributed(5, cmd)

"""

resultFile = open('CL.txt','w')
regex = re.compile('(predict)(\d+\.?\d*)(\.out)')
for corpus in corpora:
    print "\n" +corpus
    for foretell in glob.glob(base +predict +os.sep +corpus +os.sep +"predict*"):
        lamda = regex.search(os.path.basename(foretell)).group(2)
        estimate = base +predict +os.sep +corpus +os.sep +"threshold" +lamda +".out"

        f= open(estimate)
        p = []
        c = []
        print estimate
        for line in f: #Very slow
            c.append(float(line.split(" ")[1]))
            p.append(float(line.split(" ")[2][:-1]))
        F, prec, rec, threshold = optimalFThreshold(p,c)
        f.close()

        f= open(foretell)
        auc= readAUC(f)
        f.close()
        
        f= open(foretell)
        F, prec, rec = readResults(f,threshold)
        f.close()

        f= open(foretell)
        TP, FP, FN, TN = getAbsoluteNumbers(f,threshold)
        f.close()

        resultFile.write("insert into ppiCL (corpus, parsertype, parser, kernel, normalized, c, kernel_script) values ('" +corpus +"', 'dependency', 'Charniak-Lease+Stanford converter', 'APG', 't', " +lamda +", 'allgraph:" +lamda +" " +tokenizer +" " +normalized  +")');\n")

        f= open(foretell)
        for line in f:
            array=line.split()
            resultFile.write("insert into ppiCLoutput (expId, pair, output, prediction) values (currval('ppiCL_ppiCLid_seq'), '" +array[0] +"', '" +array[1] +"', " +array[2] +");\n")
        f.close()

        resultFile.write("update ppiCL set tp = " +str(TP)  +", fn = " +str(FN) +", tn = " +str(TN) +", fp = " +str(FP) +", total = " +str(TP+FN+TN+FP) +", auc = " +str(auc)  +", precision_ = " +str(prec) +", recall = " +str(rec) +", f_measure = " +str(F) +" where ppiCLid = currval('ppiCL_ppiCLid_seq');")


resultFile.close()

