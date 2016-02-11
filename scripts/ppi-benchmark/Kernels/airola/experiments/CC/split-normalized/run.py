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

base="/vol/home-vol3/wbi/thomas/workspace/Kernels/airola/experiments/CC/split-normalized/"
tokenizer="split"
parser="split_parse"



splits="corpus" 
dictionary="dictionary" #subfolder contains all dictionaries
linearized="linearized" #Subfolder containing the linearized features
normalized="normalized" #Subfolder containing the normalized linearized features
trained="trained"       #Subfolder containing the trained 
predict="predict"       #Subfolder containing the predicted values

corpora= os.listdir(base+splits) #Contains all five corpora

#First Step; generate a dictionary for each train[0-9].txt

print "Step1: Generating Dictionary"
cmd =[]
for corpus in corpora:
    print corpus
    train = base +splits +os.sep +corpus +os.sep +"corpus.xml.gz"
    dict = base + splits +os.sep +corpus +os.sep +"dict.gz"
    cmd.append("python " +source +os.sep + "BuildDictionaryMapping.py -p " +parser +" -t " +tokenizer +" -i " +train  +" -o " +dict)
runDistributed(5, cmd)


#Step Two: Generate 
#compute the graph kernels for your data, producing a linearized feature representation corresponding to the graph kernels.
print "Step2: Generating linearized feature representation"
cmd =[]
for corpus in corpora:
    print "\n" +corpus
    dict= base + splits +os.sep +corpus +os.sep +"dict.gz" 
    os.makedirs(base +linearized +os.sep +corpus)

    for linearize in corpora:
        print "Linearizing " +linearize
        input = base + splits +os.sep +linearize +os.sep +"corpus.xml.gz"
        out = base +linearized +os.sep +corpus +os.sep +linearize +".gz"
        cmd.append("python " +source +os.sep + "LinearizeAnalysis.py -p " +parser +" -t " +tokenizer +" -d " +dict +" -i " +input +" -o " +out)
runDistributed(8, cmd) 


#Step Three: you can normalize the data vectors to unit length. Sometimes this can boost the results, sometimes it makes them worse.
print "Step3:Normalize data"
cmd= []
for corpus in corpora:
    print "\n" +corpus
    os.makedirs(base +normalized +os.sep +corpus)

    for data in glob.glob(base +linearized +os.sep +corpus +os.sep +"*.gz"): #Iterate over all Splits
        print "Normalizing:" +os.path.basename(data)
        cmd.append("python " +source +os.sep + "NormalizeData.py -i" +data +" -o " +base + normalized +os.sep +corpus +os.sep + os.path.basename(data))
runDistributed(8, cmd)        


#Step4: Train a  model for each trainingset
print "Step4: Train a model for each Trainingset"
cmd=[] #Put all commands in a 
for corpus in corpora: #Iterate over corpora
    print corpus
    for train in glob.glob(base +normalized +os.sep +corpus +os.sep +corpus +".gz"): #Iterate over Traindata
#        print train

        dir= base +trained +os.sep +corpus +os.sep
        os.makedirs(dir)

        for l in range(-2,2): #Gridsearch
            lamda= pow(2,l) 
            cmd.append("python " +source +os.sep +"TrainLinearized.py -r " +str(lamda) +" -i " +train +" -o "  +dir + "train" +str(lamda) +".model")

runDistributed(8, cmd)


print "Step 5 predict!"
cmd= []
regex = re.compile('(train)(\d+\.?\d*)(\.model)')
for corpus in corpora:
    print "\n" +corpus
    for split in glob.glob(base +trained +os.sep +corpus +os.sep +"*.model"):
        model = split
        split= os.path.basename(split)
        print "\n" +split
        for p in corpora:
                
            outdir= base +predict+os.sep+corpus+os.sep +p +os.sep
            try:
                os.makedirs(outdir)
            except OSError:
                print "np"
            lamda = regex.search(os.path.basename(split)).group(2)
            cmd.append("python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +p +".gz"  +" -m " +model  +" -o " +outdir +"predict"+ lamda+".out")
                        
runDistributed(8, cmd)



p = []
c = []
dict = {}
fulldict= {}
lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')
for corpus in corpora:
    for predicted in corpora:
        if predicted == corpus:
            dict= {} #Reset the dictionary
            for foretell in glob.glob(base +predict +os.sep +corpus +os.sep +predicted +os.sep +"*"):
                f= open(foretell)
                for line in f:
                    c.append(float(line.split(" ")[1]))
                    p.append(float(line.split(" ")[2][:-1]))
                l= lambdaRegex.search(os.path.basename(foretell)).group(2) 
                F, prec, rec, threshold = optimalFThreshold(p,c)
                dict[l]= threshold
#                print corpus +" l=" +l   +" " +str(threshold)
            #print dict
            fulldict[corpus] = dict
#print fulldict

print "Step 6 estimate quality!"
#regex = re.compile('(train)(\d+)')
lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')
resultFile = open('CC.txt','w')
for corpus in corpora:
    print "\n" +corpus
    for predicted in corpora:
        if predicted != corpus:
            print predicted
            for foretell in glob.glob(base +predict +os.sep +corpus +os.sep +predicted +os.sep +"*"): 
                lam=lambdaRegex.search(os.path.basename(foretell)).group(2)
                print lam
                threshold=fulldict.get(corpus).get(lam)
                
                #F-Meausure, Precision, and so on
                f= open(foretell)
                F, prec, rec = readResults(f,threshold)
                f.close()
                
                #TP,TN,FN and FP
                f= open(foretell)
                TP, FP, FN, TN = getAbsoluteNumbers(f,threshold)
                f.close()
                
                #AUC
                f= open(foretell)
                auc= readAUC(f)
                f.close()

                resultFile.write("insert into ppiCC (corpus, test, parsertype, parser, kernel, normalized, c, kernel_script) values ('" +corpus +"', '" +predicted +"', 'dependency', 'Charniak-Lease+Stanford converter', 'APG', 't', " +lam +", 'allgraph:" +lam +" " +tokenizer +" normalized"  +"');\n")

                f= open(foretell)
                for line in f:
                    array=line.split()
                    resultFile.write("insert into ppiCCoutput (expId, pair, output, prediction) values (currval('ppiCC_ppiCCid_seq'), '" +array[0] +"', '" +array[1] +"', " +array[2] +");\n")
                
                resultFile.write("update ppiCC set  tp = " +str(TP) +", fn = " +str(FN) +", tn = " +str(TN) +", fp = " +str(FP) +", total = " +str(TP+FN+TN+FP)  +", auc = " +str(auc) +", precision_ = " +str(prec) +", recall = " +str(rec) +", f_measure = " +str(F) +" where ppiCCid = currval('ppiCC_ppiCCid_seq');")
                           
resultFile.close()


