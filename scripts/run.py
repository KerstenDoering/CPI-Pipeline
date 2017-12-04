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
base= path +os.sep +str(sys.argv[1])+'/'
print "base:",base
sys.path.append(source +'/measures/')
# limit number of processes
max_proc_count = multiprocessing.cpu_count()
# limit number of documents per file- this for avoiding the problem of insufficient of memory
limitToSplit = 20000

from distributed import *
from PerformanceMeasures import computeAUC
from Fscore import *
from Utilities import optimalFThreshold

import subprocess
from subprocess import PIPE

def readAUC(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc


def splitTestDataSet():

    for corpus in corpora:
        
        
        pathN = base + normalized +os.sep +corpus +os.sep
        os.chdir(pathN)
        
        os.system('zcat test0.txt.gz | wc -l')
        cmd = "zcat test0.txt.gz | split -d -a 2 -l "+ str(limitToSplit) + " - temp --filter='gzip > $FILE.txt.gz'"
        os.system(cmd)



        os.system("rm test0.txt.gz")

        reg = re.compile('(temp)(\d+)(\.txt)(\.gz)')
        for filename in glob.glob("temp*.txt.gz"): #Iterate over Traindata    
            file_number = reg.search(filename).group(2)
            
            new_name = "test"+str(file_number)+".txt.gz"
            shutil.move(filename, new_name)

    os.chdir(base)    

# measure programme start time
start = time.asctime()

tokenizer=os.environ["TOKENIZER"]
parser=os.environ["PARSER"]

splits="corpus"         #subfolder, where the splits are
dictionary="dictionary" #subfolder contains all dictionaries
linearized="linearized" #Subfolder containing the linearized features
normalized="normalized" #Subfolder containing the normalized linearized features
trained="trained"       #Subfolder containing the trained 
predict="predict"       #Subfolder containing the predicted values

corpora= os.listdir(base+splits) #Contains all five corpora






#First Step; generate a dictionary for each training data set
print "\nStep1: Generating Dictionary"
print "-----------------------------\n"
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


'''
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
'''

#Step Two: Generate 
#compute the graph kernels for your data, producing a linearized feature representation corresponding to the graph kernels.
print "\nStep2: Generating linearized feature representation"
print "----------------------------------------------------------\n"
cmd =[]
for corpus in corpora:

    os.makedirs(base +linearized +os.sep +corpus)
    for data in glob.glob(base+splits +os.sep +corpus +os.sep +"*.gz"): #Iterate over all Splits
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



'''

cmd = "ls " + base + linearized +os.sep +corpus

os.system(cmd)
cmd = "cat "+ base + linearized +os.sep +corpus +os.sep +"test* >"+ base + linearized +os.sep +corpus +os.sep +"temp.txt.gz"

os.system(cmd)

cmd = "rm "+ base + linearized +os.sep +corpus +os.sep +"test*"
os.system(cmd)

cmd = "mv "+ base + linearized +os.sep +corpus +os.sep +"temp.txt.gz " + base + linearized +os.sep +corpus +os.sep +"test0.txt.gz"
os.system(cmd)
'''

#Step Three: you can normalize the data vectors to unit length. Sometimes this can boost the results, sometimes it makes them worse.
print "\nStep3: Normalize data"
print "-----------------------\n"
cmd= []
for corpus in corpora:

    os.makedirs(base +normalized +os.sep +corpus)
    for data in glob.glob(base +linearized +os.sep +corpus +os.sep +"*.gz"): #Iterate over all Splits
        print os.path.basename(data)

        cmd.append("python " +source +os.sep + "NormalizeData.py -i" +data +" -o " +base + normalized +os.sep +corpus +os.sep + os.path.basename(data))
        

runDistributed(min(max_proc_count, len(cmd)), cmd)





#Step4: Train a  model for each trainingset
print "\nStep4: Train a model for each Trainingset"
print "-------------------------------------------\n"
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



#splitTestDataSet()
     


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
    
'''    
    
    for split in glob.glob(base +trained +os.sep +corpus +os.sep +"*"):
        split= os.path.basename(split)
        outdir= base +predict+os.sep+corpus+os.sep+split+os.sep
        os.makedirs(outdir)
        for model in glob.glob(base +trained +os.sep +corpus +os.sep +split +os.sep +"*.model"):
            lamda = regex.search(os.path.basename(model)).group(2)
            print "lamda :", lamda
            ##cmd.append("python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"test" +split[5:] +".txt.gz"  +" -m " +model  +" -o "  +outdir+"predict"+lamda+".out")
            print model
            cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"test" +split[5:] +".txt.gz"  +" -m " +model  +" -o "  +outdir+"predict"+lamda+".out"
            print "cmd:", cmd
            process = subprocess.call(cmd, shell=True)
            
            ##cmd.append("python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out")    
            train_fname = base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"
            if (os.path.isfile(train_fname)):         
                cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out"
            else:
                cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train0.txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out"    
            print "cmd:", cmd
            process = subprocess.call(cmd, shell=True)                      
#runDistributed(5, cmd)


print "Step 5: predict!"
cmd= []
regex = re.compile('(train)(\d+\.?\d*)(\.model)')
for corpus in corpora:
    print corpus
    for split in glob.glob(base +trained +os.sep +corpus +os.sep +"*"):
        split= os.path.basename(split)
        outdir= base +predict+os.sep+corpus+os.sep+split+os.sep
        os.makedirs(outdir)
        for model in glob.glob(base +trained +os.sep +corpus +os.sep +split +os.sep +"*.model"):
            lamda = regex.search(os.path.basename(model)).group(2)
            print "lamda :", lamda
            ##cmd.append("python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"test" +split[5:] +".txt.gz"  +" -m " +model  +" -o "  +outdir+"predict"+lamda+".out")
            print model
            cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"test" +split[5:] +".txt.gz"  +" -m " +model  +" -o "  +outdir+"predict"+lamda+".out"
            print "cmd:", cmd
            process = subprocess.call(cmd, shell=True)
            
            ##cmd.append("python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out")    
            train_fname = base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"
            if (os.path.isfile(train_fname)):         
                cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train" +split[5:] +".txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out"
            else:
                cmd = "python " +source +os.sep +"TestLinearized.py -i " +base +normalized +os.sep +corpus +os.sep +"train0.txt.gz"  +" -m "+model  +" -o "  +outdir+"threshold"+lamda+".out"    
            print "cmd:", cmd
            process = subprocess.call(cmd, shell=True)                      
#runDistributed(5, cmd)

'''

def getThreshold(f):
    f= open(estimate)
    p = [] #predict
    c = [] #class
    for line in f:
        c.append(float(line.split(" ")[1]))
        p.append(float(line.split(" ")[2][:-1]))
    F, prec, rec, threshold = optimalFThreshold(p,c)
    f.close()
    return threshold

print "Ste6 estimate quality"
print "Step 6 estimate quality!"                                                                                                                            

regex = re.compile('(train)(\d+)')
lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')


for corpus in corpora: #Iterate corpora
    #print corpus
    resultFile = open(corpus+'.sql','w')
    for split in glob.glob(base +predict +os.sep +corpus +os.sep +"*"): #Iterate the CV-splits
        splitname=regex.search(os.path.basename(split)).group(2) #current split

        for foretell in glob.glob(split +os.sep +"predict*.out"):  #Iterate over the different lambda params
#            print foretell, "##"
            lamd=lambdaRegex.search(os.path.basename(foretell)).group(2) #Extract the lambda-setting
            resultFile.write("insert into ppiCV  (corpus, parsertype, parser, kernel, fold, normalized, c, kernel_script) values ('"+corpus +"', 'dependency', 'Charniak-Lease+Stanford converter', 'APG', " +splitname +", 't', " +lamd +", 'allgraph:" +lamd +" " +tokenizer +" " +"normalized" +"');\n")

            estimate= split +os.sep +"threshold" +lamd +".out" #File needed to estimate the threshold; (selfprediction!)
#            print corpus +" " +str(splitname) +"/" +str(9) +" lambda=" +lamd           

            threshold= getThreshold(estimate) #Get the optimal threshold setting
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

# measure programme end time
end = time.asctime()

# print start and and time
print "programme started - " + start
print "programme ended - " + end

#'''

"""
print "Step 6 estimate quality!"
regex = re.compile('(train)(\d+)')
lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')
resultFile = open('out.txt','w')
for corpus in corpora:
    print corpus
    for split in glob.glob(base +predict +os.sep +corpus +os.sep +"*"): #Iterate over splits
        splitname=regex.search(os.path.basename(split)).group(2) #Which Split?                                                                             
        for foretell in glob.glob(split +os.sep +"predict*.out"):  #Iterate over the different lambda params
            lamd=lambdaRegex.search(os.path.basename(foretell)).group(2) #What Lambda param?
            estimate= split +os.sep +"threshold" +lamd +".out" #File needed to estimate the threshold
            print corpus +" " +str(splitname) +"/" +str(9) +" lambda=" +lambdaRegex.search(os.path.basename(foretell)).group(2)
            threshold= getThreshold(estimate)
            f= open(foretell)
            F, prec, rec = readResults(f,threshold)
            f.close()
            f= open(foretell)
            auc= readAUC(f)
            f.close()#AUC is always the same, independant from threshold
            resultFile.write("INSERT INTO exb (parser, model, corpus,  fold, kernel) VALUES ('Version06', 'best', '" +corpus +"', "+splitname +", 6);\n")
            resultFile.write("UPDATE exb set kernel_script = '" +"allgraph:" + lambdaRegex.search(os.path.basename(foretell)).group(2) +" " +tokenizer +" normalized" +" t=neq0"  +"'" +" WHERE exbid = currval('exb_exbid_seq');"  +"\n")
            resultFile.write("UPDATE exb set auc = " +str(auc) +" ,precision_ = " +str(prec) +" ,recall = " +str(rec) +" ,f_measure = " +str(F) +" WHERE exid = currval('exb_exbid_seq');\n\n")
resultFile.close()
"""








"""
print "Step 6 estimate quality!"
regex = re.compile('(train)(\d+)')
lambdaRegex = re.compile('(predict)(\d+\.?\d*)(.out)')
resultFile = open('out.txt','w')
for corpus in corpora:
    print corpus
    for split in glob.glob(base +predict +os.sep +corpus +os.sep +"*"):
        splitname=regex.search(os.path.basename(split)).group(2)
        for foretell in glob.glob(split +os.sep +"*.out"):
            f= open(foretell)
            auc= readAUC(f)
            f.close()
            f= open(foretell)
            p = []
            c = []
            for line in f:
                c.append(float(line.split(" ")[1]))
                p.append(float(line.split(" ")[2][:-1]))
            F, prec, rec, threshold = optimalFThreshold(p,c)
            f.close()
            print corpus +" " +str(splitname) +"/" +str(9) +" lambda=" +lambdaRegex.search(os.path.basename(foretell)).group(2)
            f= open(foretell)
            F, prec, rec = readResults(f,threshold)
            f.close()
            resultFile.write("INSERT INTO exb (parser, model, corpus,  fold, kernel) VALUES ('Version06', 'best', '" +corpus +"', "+splitname +", 6);\n")
            resultFile.write("UPDATE exb set kernel_script = '" +"allgraph:" + lambdaRegex.search(os.path.basename(foretell)).group(2) +" " +tokenizer +" normalized" +" t=neq0"  +"'" +" WHERE exbid = currval('exb_exbid_seq');"  +"\n")
            resultFile.write("UPDATE exb set auc = " +str(auc) +" ,precision_ = " +str(prec) +" ,recall = " +str(rec) +" ,f_measure = " +str(F) +" WHERE exbid = currval('exb_exbid_seq');\n\n")
resultFile.close()
"""
