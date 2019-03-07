#!/usr/bin/python
#nice python run.py 1>run.out 2>run.err
import os
import glob
import subprocess
import re
import math
import sys
import os.path
import datetime
import time
import shutil
import locale
locale.setlocale(locale.LC_ALL, '')

sys.path.append('..') 
from jsreconfig import *

from convert import *
from addids import *
from distributed import *
from PerformanceMeasures import computeAUC
from Fscore import *

limitToSplit =10000

expTyp = str(sys.argv[1])
realnameDS = str(sys.argv[2])
realnameDS='CPI-DS_IV'
corpus = "DS"

base = basepath + os.sep + expTyp + os.sep
splits = base + 'corpus'
trained = base + 'trained'
predict = base + 'predict'
result = base + 'output.sql'



def readAUC(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        if(int(line[0].split('.')[1][1:])>=830):
            continue	
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc

# This function to split the dataset into small chuncks to avoid the problem of insufficient memory
def Splitting():


    cmd = "cat "+ splits +os.sep +corpus +os.sep +"test* >"+ splits +os.sep +corpus +os.sep +"temp.txt"

    os.system(cmd)

    cmd = "rm "+ splits +os.sep +corpus +os.sep +"test*"
    os.system(cmd)

    cmd = "split -d -a 4 -l "+ str(limitToSplit) + " --additional-suffix=.txt " + splits +os.sep +corpus +os.sep + "temp.txt " + splits +os.sep +corpus +os.sep + "test"
    os.system(cmd)


    cmd = "rm "+ splits +os.sep +corpus +os.sep +"temp.txt"
    os.system(cmd)



#Train a Model
def Training(w0,w1,n0,n1):
    
    #if expTyp == 'CV':
        #w0,w1,n0,n1 = 1,4,1,4
    
    if expTyp == 'PR':
        # copy the training model (w=1 &  n=3), this experiment(PR) will use the already built model.
        scr="../../../../training_model/SL_PR_training/trained_model"
        dest=trained
        shutil.copytree(scr, dest)
        return
    
    elif expTyp == 'XX':
    
        scr="../../../Corpora/train0.txt"
        dest=splits +os.sep +corpus +os.sep
        print dest
        shutil.move(scr, dest)  
        #w0,w1,n0,n1 = 1,2,3,4

    
    cmd = []
    regex = re.compile('\D+\d+')

    for corpus_t in corpora:
        for train in glob.glob(splits + os.sep + corpus_t + os.sep + "train*.txt"): #Iterate over Traindata        
            trainName = os.path.basename(train)
            trainName = regex.search(os.path.basename(trainName)).group(0) #For example train[0-9]
            
            dir = trained + os.sep + corpus_t + os.sep + trainName + os.sep
            os.makedirs(dir)
            start = time.time()
    #        for w in range(1,4):
    #            for n in range(1,4):
    #                print("w=" +str(w) +" n=" +str(n))
    #        cmd.append("java -classpath /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/bin/:/vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/lib/* -mx1024M org.itc.irst.tcc.sre.Train -m 512 -k SL -n " +str(n) +" -w " +str(w) +" " +train +" " +dir+"trainn\="+str(n) +"w\=" +str(w) +".model")

            os.chdir(jsre)

            # Kersten: changed command to use newly exported jar file for training with debugged code which really uses window size and n-gram
    #        job = subprocess.Popen("java -classpath '" + jsre_classpath + "' -mx8024M org.itc.irst.tcc.sre.Train -m 512 -k SL -n " + str(n) + " -w " + str(w) + " " + train + " " + dir + "trainn\=" + str(n) + "w\=" + str(w) + ".model", shell=True)
            for w in range(w0,w1):
                for n in range(n0,n1):
                    cmd.append("java -jar " + jsre_classpath_train + " -n " + str(n) + " -w " + str(w) + " " + train + " " + dir + "trainn\=" +      str(n) + "w\=" + str(w) + ".model")
                    job = subprocess.Popen("java -jar " + jsre_classpath_train + " -n " + str(n) + " -w " + str(w) + " " + train + " " + dir + "trainn\=" +      str(n) + "w\=" + str(w) + ".model", shell=True)

            job.wait()
            end = time.time()

    #os.chdir(jsre)
    #runDistributed(4, cmd)  


def Predicting():
    cmd = []
    regex = re.compile('(trainn=)(\d+)(w=)(\d)(\.model)')
    regex_sgmnt = re.compile('(test)(\d+)(\.txt)')

    for corpus_t in corpora:
        print corpus_t
        for test in glob.glob(splits +os.sep +corpus_t +os.sep +"test*"):

            print test
            sgmnt = regex_sgmnt.search(os.path.basename(os.path.basename(test))).group(2)

            outdir= predict+os.sep+corpus_t+os.sep+"train"+sgmnt+os.sep

            os.makedirs(outdir)

            dname = trained +os.sep +corpus_t +os.sep +"train" + sgmnt
            print dname
            if (os.path.isdir(dname)):
                trainDir = "train" + sgmnt
            
            else:
                trainDir = "train0"


            for model in glob.glob(trained + os.sep + corpus_t + os.sep + trainDir + os.sep + "*.model"):
                n = regex.search(os.path.basename(model)).group(2)
                w = regex.search(os.path.basename(model)).group(4)

    #            print("java -classpath /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/bin/:/vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/lib/* -mx1024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")

                cmd.append("java -classpath '" + jsre_classpath + "' -mx2024M org.itc.irst.tcc.sre.Predict " +test   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")

                os.chdir(jsre)
                job=subprocess.Popen("java -classpath '" + jsre_classpath + "' -mx8024M org.itc.irst.tcc.sre.Predict " +test   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out",shell=True)
                job.wait()


    #os.chdir(jsre)
    #runDistributed(4, cmd)


# This fuction to evaluate the prediction
def Evaluating():

    print "Step 3 evaluate!"
    cmd = []
    regex = re.compile('predictn=(\d+)w=(\d+)\.out')
    resultFile = open(result, 'w')
    resultFile.write("-- Date created:  " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + "\n\n")
    threshold = 0.
    for corpus_t in corpora:
        for split in glob.glob(predict + os.sep + corpus_t + os.sep + "*"):
            split = os.path.basename(split)
            fold = split[5:]
            print corpus_t, split
            for prediction in glob.glob(predict + os.sep + corpus_t + os.sep + split + os.sep + "*.out"):
                resultFile.write("-- BEGIN experiment -- corpus: '" + corpus_t + "', split: '" + split + "', fold: '" + fold + "', prediction file: '" + prediction + "'\n")
                n = regex.search(os.path.basename(prediction)).group(1)
                w = regex.search(os.path.basename(prediction)).group(2)
                print n,w 
                print "###", prediction
                convert(prediction) #Convert into expected data format


                # write single predictions
                test = splits + os.sep + corpus_t + os.sep + 'test' + fold + '.txt' # same as in Step 2 predict
                addids(prediction, test) # Replace sequence number with original pair IDs from			

                f = open(prediction)
                # change:
                try:
                    auc= readAUC(f)
                except:
                    auc = "Null"
                    #print "no auc, division by zero", "#####"
                f.close()
                f = open(prediction)
                F, prec, rec, TP, FP, FN, TN = readResults(f, threshold)
                f.close()
                #print auc, F, prec, rec

                # write experiment parameters

                resultFile.write("INSERT INTO ppiCV (parsertype, parser, corpus, fold, kernel, kernel_script, forced_threshold) " + 
		     "VALUES ('POS tagger', 'TextPRO (Version06?)', '" + realnameDS + "', " + fold + ", 'SL', 'jsre; n=" + n + " (n-gram), w=" + w + " (window)', 0.0);\n")
                
                # write experiment evaluation data
                resultFile.write("UPDATE ppiCV SET tp = " +str(TP) +", fn = " +str(FN) +", tn = " +str(TN) +", fp = " +str(FP) +", total = " +str(TP+TN+FP+FN) +", auc = " + str(auc) + " , precision_ = " + str(prec) + " , recall = " + str(rec) + ", f_measure = " + str(F) + " WHERE ppiCVid = currval('ppiCV_ppiCVid_seq');\n")

               
                f = open(prediction)
                for line in f:
                    line = line.split()
                    if(int(line[0].split('.')[1][1:])>=830):
                        continue	
                   
                    # example line: "9 1.0 0.586770226173"
                    if float(line[2]) >= threshold:
                        insertString = '1'
                    else:
                        insertString = '0'
                    
                    resultFile.write("INSERT INTO ppiCVoutput (expId, pair, output, prediction) VALUES (currval('ppiCV_ppiCVid_seq'), '" + line[0] + "', '" + insertString + "', " + line[2] + ");\n")
                f.close() 

                resultFile.write("-- END experiment\n\n")

    resultFile.close



if __name__ == "__main__":

    

    corpora = os.environ["CORPORA"].split() #Contains the corpora

    #print "AAAAAAAAAAAAAAAAA:", corpora
    print "Step1-Training"
    Training(1,4,1,4)
    
    if expTyp in ['PR', 'XX']:
        Splitting()
        
    print "Step 2 predict!"
    Predicting()
    
    Evaluating()

