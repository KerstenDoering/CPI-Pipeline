#!/usr/bin/python
#python run.py 1>run.out 2>run.err
#This script trains a kernel 
import os
import glob
import subprocess
import re
import time
import math
import sys
import os.path
import shutil
sys.path.append('..')
from apgconfig import *
import multiprocessing

#source='/vol/home-vol3/wbi/thomas/workspace/Kernels/airola/source' #Now defined in ../apgconfig.py
#base="/vol/home-vol3/wbi/thomas/workspace/ppi-benchmark/Experiments/apg/CV/" 
expTyp = str(sys.argv[1])
base= path +os.sep +expTyp+'/'
print "base:",base
sys.path.append(source +'/measures/')
# limit number of processes
max_proc_count = multiprocessing.cpu_count()
# limit number of documents per file- this for avoiding the problem of insufficient of memory
limitToSplit = 10000

from distributed import *
from PerformanceMeasures import computeAUC
from Fscore import *
from Utilities import optimalFThreshold

import subprocess
from subprocess import PIPE

tokenizer=os.environ["TOKENIZER"]
parser=os.environ["PARSER"]

splits="corpus"         #subfolder, where the splits are
dictionary="dictionary" #subfolder contains all dictionaries
linearized="linearized" #Subfolder containing the linearized features
normalized="normalized" #Subfolder containing the normalized linearized features
trained="trained"       #Subfolder containing the trained 
predict="predict"       #Subfolder containing the predicted values

corpora= os.listdir(base+splits)



def readAUC(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc

# Split the very large normalized test data set into smaller chunks to avoid the problem of  insufficient memory
def SplitNormDataSet():

    for corpus in corpora:
        
        
        pathN = base + normalized +os.sep +corpus +os.sep
        os.chdir(pathN)
        
        os.system('zcat test0.txt.gz | wc -l')
        cmd = "zcat test0.txt.gz | split -d -a 4 -l "+ str(limitToSplit) + " - temp --filter='gzip > $FILE.txt.gz'"
        os.system(cmd)



        os.system("rm test0.txt.gz")

        reg = re.compile('(temp)(\d+)(\.txt)(\.gz)')
        for filename in glob.glob("temp*.txt.gz"): #Iterate over Traindata    
            file_number = reg.search(filename).group(2)
            
            new_name = "test"+str(file_number)+".txt.gz"
            shutil.move(filename, new_name)

    os.chdir(base)    


# Split the very large test data set into smaller chunks to avoid the problem of  insufficient memory
def SplitTestDataSet():
    corpus = 'DS'
    # Split the very large test data set into smaller chunks to avoid the problem of  insufficient memory
    print "\nSplitting test data set ..."
    cmd= "python " + base + "xmlsplitter.py -c " + corpus
    os.system(cmd)

    cmd = "rm "+ base+splits +os.sep +corpus +os.sep +"test*.gz"
    os.system(cmd)

    cmd = "mv "+ base+splits +os.sep +corpus +os.sep + corpus + os.sep + "* " + base+splits +os.sep +corpus +os.sep

    os.system(cmd) 


    cmd = "rm -r "+ base+splits +os.sep +corpus +os.sep +corpus+os.sep
    os.system(cmd)




#First Step; generate a dictionary for each training data set
def GenerateDict():
    print "\nStep1: Generating Dictionary"
    print "-----------------------------\n"

    startDict = time.asctime()
    
    if expTyp == 'PR':
        corpus = 'DS'
        os.makedirs(base + dictionary+os.sep+corpus)
        cmd = "cp ../../../../training_model/APG_PR_training/Dict_train0.txt.gz "+ dictionary + os.sep + corpus + os.sep + "train0.txt.gz"
        os.system(cmd)
        print "Done..."
        return
        

    

    cmd =[]
    for corpus in corpora:
        #print corpus
        os.makedirs(base +dictionary +os.sep +corpus)

        #Iterate over the Training files in Split
        print base+splits +os.sep +corpus +os.sep +"train*.gz"
        for train in glob.glob(base+splits +os.sep +corpus +os.sep +"train*.gz"):
            print os.path.basename(train)

            dict = base+dictionary+os.sep +corpus+os.sep+os.path.basename(train)
            cmd.append("python " +source +os.sep + "BuildDictionaryMapping.py -p " +parser +" -t " +tokenizer +" -i " +train +" -o " + dict)

    runDistributed(min(max_proc_count, len(cmd)), cmd)

    endDict = time.asctime()

    print "Start Generating Dictionary at  " + startDict
    print "End Generating Dictionary at  " + endDict




#Step Two: Compute the graph kernels for your data, producing a linearized feature representation corresponding to the graph kernels.
def Linearization():
    print "\nStep2: Generating linearized feature representation"
    print "----------------------------------------------------------\n"

    startLinear = time.asctime()

    cmd =[]
    for corpus in corpora:

        os.makedirs(base +linearized +os.sep +corpus)
        if expTyp == 'PR':
            dataset = base+splits +os.sep +corpus +os.sep +"test*.gz"
        else:
            dataset = base+splits +os.sep +corpus +os.sep +"*.gz"
                
        for data in glob.glob(dataset): #Iterate over all Splits
            print os.path.basename(data)
            
            input = data
            out = base+linearized+os.sep +corpus+os.sep+os.path.basename(data)
            
            number_regex = re.compile('\d+')

            fname = base +dictionary +os.sep +corpus +os.sep +"train" + number_regex.search(os.path.basename(data)).group(0)+".txt.gz"
            
            if (os.path.isfile(fname)):
                dict = fname

            else:
                dict = base +dictionary +os.sep +corpus +os.sep +"train0.txt.gz"

            cmd.append("python " +source +os.sep + "LinearizeAnalysis.py -p " +parser +" -t " +tokenizer  +" -i " + input +" -o " + out +" -d " + dict) 

    runDistributed(min(max_proc_count, len(cmd)), cmd)

    endLinear = time.asctime()

    
    if expTyp == 'PR':
        cmd = "cp ../../../../training_model/APG_PR_training/Linearized_train0.txt.gz "+ linearized + os.sep + corpus + os.sep + "train0.txt.gz"
        os.system(cmd)

        
    print "Start Generating linearized feature at - " + startLinear
    print "End Generating linearized feature at - " + endLinear



#Step Three: you can normalize the data vectors to unit length. Sometimes this can boost the results, sometimes it makes them worse.
def Normalization():
    startNorm = time.asctime()

    print "\nStep3: Normalize data"
    print "-----------------------\n"
    cmd= []
    for corpus in corpora:

        os.makedirs(base +normalized +os.sep +corpus)
        if expTyp == 'PR':
            dataset = base + linearized + os.sep +corpus + os.sep +"test*.gz"
        else:
            dataset = base + linearized +os.sep + corpus + os.sep +"*.gz"
            
        for data in glob.glob(dataset): #Iterate over all Splits
            print os.path.basename(data)

            cmd.append("python " +source +os.sep + "NormalizeData.py -i" +data +" -o " +base + normalized +os.sep +corpus +os.sep + os.path.basename(data))
            

    runDistributed(min(max_proc_count, len(cmd)), cmd)

    endNorm = time.asctime()

    if expTyp == 'PR':
        scr="../../../../training_model/APG_PR_training/Norm_train0.txt.gz"
        dest=normalized + os.sep + corpus + os.sep + "train0.txt.gz"
        shutil.copy(scr, dest)
        
    print "Start Normalize data at :" + startNorm
    print "End Normalize data at :" + endNorm


#Step4: Train a  model for each trainingset
def Training():
    print "\nStep4: Train a model for each Trainingset"
    print "-------------------------------------------\n"

    startTraining = time.asctime()
       
    if expTyp == 'PR':
        scr="../../../../training_model/APG_PR_training/trained_model"
        dest=trained
        shutil.copytree(scr, dest)
        print "Done..."
        return

    # else For expTyp in [CV, XX]
    regex = re.compile('\D+\d+')
    cmd=[] #Put all commands in a 
    for corpus in corpora: #Iterate over corpora

        for train in glob.glob(base +normalized +os.sep +corpus +os.sep +"train*.gz"): #Iterate over Traindata
            trainName= os.path.basename(train)
            trainName= regex.search(os.path.basename(trainName)).group(0) #For example train[0-9]
      
            dir= base +trained +os.sep +corpus +os.sep +trainName +os.sep
            os.makedirs(dir)

            for l in range(-2,2): #Gridsearch
                lamda= pow(2,l) 

                cmd.append("python " +source +os.sep +"TrainLinearized.py -b 2000 -r " +str(lamda) +" -i " +train +" -o "  +dir + "train" +str(lamda) +".model")


    runDistributed(min(max_proc_count, len(cmd)), cmd)

    endTraining = time.asctime()
    print "Start Train a model at :" , startTraining
    print "End Train a model at :" , endTraining


#Step5: Predict each ineraction based on the training model
def Predicting():

    startPrediction = time.asctime()
    print "\nStep 5: predict!"
    print "------------------\n"
    cmd= []
    regex_sgmnt = re.compile('(test)(\d+)(\.txt)(\.gz)')
    regex_lamda = re.compile('(train)(\d+\.?\d*)(\.model)')
    for corpus in corpora:

        for test in glob.glob(base +normalized +os.sep +corpus +os.sep +"test*"):
            

            sgmnt = regex_sgmnt.search(os.path.basename(os.path.basename(test))).group(2)

            outdir= base +predict+os.sep+corpus+os.sep+"train"+sgmnt+os.sep

            os.makedirs(outdir)
            
            fname = base +normalized +os.sep +corpus +os.sep +"train" + sgmnt +".txt.gz"
            if (os.path.isfile(fname)):
                train = fname

            else:
                train = base +normalized +os.sep +corpus +os.sep +"train0.txt.gz"

            split=(os.path.basename(train)).split(".")[0]
            for model in glob.glob(base +trained +os.sep +corpus +os.sep + split +os.sep +"*.model"): 
                lamda = regex_lamda.search(os.path.basename(model)).group(2)    
                #print test
                #print train

                cmd.append("python " +source +os.sep +"TestLinearized.py -i " + test  +" -m " + model  + " -o "  + outdir+"predict"+lamda+".out")
                cmd.append("python " +source +os.sep +"TestLinearized.py -i " + train +" -m " + model  + " -o "  + outdir+"threshold"+lamda+".out")                         


    runDistributed(min(max_proc_count, len(cmd)), cmd)

    endPrediction = time.asctime()

    print "Start predict at :" + startPrediction
    print "End predict at :" + endPrediction
    print 
    


def getThreshold(estimateFile):
    f= open(estimateFile)
    p = [] #predict
    c = [] #class
    for line in f:
        c.append(float(line.split(" ")[1]))
        p.append(float(line.split(" ")[2][:-1]))
    F, prec, rec, threshold = optimalFThreshold(p,c)
    f.close()
    return threshold



# This fuction to evaluate the prediction
def Evaluating():
    regex = re.compile('(train)(\d+)')
    lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')


    for corpus in corpora: #Iterate corpora
        resultFile = open(corpus+'.sql','w')
        for split in glob.glob(base +predict +os.sep +corpus +os.sep +"*"): #Iterate the CV-splits
            splitname=regex.search(os.path.basename(split)).group(2) #current split

            for foretell in glob.glob(split +os.sep +"predict*.out"):  #Iterate over the different lambda params
    #            print foretell, "##"
                lamd=lambdaRegex.search(os.path.basename(foretell)).group(2) #Extract the lambda-setting
                resultFile.write("insert into ppiCV  (corpus, parsertype, parser, kernel, fold, normalized, c, kernel_script) values ('"+corpus +"', 'dependency', 'Charniak-Lease+Stanford converter', 'APG', " +splitname +", 't', " +lamd +", 'allgraph:" +lamd +" " +tokenizer +" " +"normalized" +"');\n")

                estimateFile= split +os.sep +"threshold" +lamd +".out" #File needed to estimate the threshold; (selfprediction!)
    #            print corpus +" " +str(splitname) +"/" +str(9) +" lambda=" +lamd           

                threshold= getThreshold(estimateFile) #Get the optimal threshold setting
                f= open(foretell)
                for line in f:
                    array=line.split()
                    if float(array[2]) >= threshold:
                        insertString = '1'
                    else:
                        insertString = '0'
                    resultFile.write("insert into ppiCVoutput (expId, pair, output, prediction) values (currval('ppiCV_ppiCVid_seq'), '" +array[0] +"', '"+insertString +"', " +array[2] +");\n")

                f= open(foretell)
                F, prec, rec = readResults(f,threshold)
    #            print "F-score:", F, ", recall:", rec, ", precision:", prec, "###"
                f.close()

                f= open(foretell)
                TP, FP, FN, TN = getAbsoluteNumbers(f,threshold)
    #            print "TP:", TP, ", TN:", TN, ", FP:", FP, ", FN:", FN, "####"
                f.close()            
                
                f= open(foretell)
                try:
                    auc= readAUC(f)
                except:
                    auc = "Null"
    #                print "no auc, division by zero", "#####"
                f.close()


                    
                resultFile.write("update ppiCV set tp = " +str(TP) +", fn = " +str(FN) +", tn = " +str(TN) +", fp = " +str(FP) +", total = " +str(TP+TN+FP+FN) +", auc = " +str(auc) +", precision_ = " +str(prec) +" , recall = " +str(rec) +", f_measure = " +str(F) +" where ppiCVid = currval('ppiCV_ppiCVid_seq');\n")
        resultFile.close()



if __name__ == "__main__":

    if expTyp in  ['CV', 'PR', 'XX']:
        
        GenerateDict()
        Linearization()
        Normalization()
        Training()
        if expTyp in  ['PR', 'XX']:
            SplitNormDataSet()
        Predicting()
        Evaluating()
        
    else:
    
        print "Invalid expTyp :", expTyp , " !"
