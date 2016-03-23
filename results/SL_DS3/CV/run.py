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
import locale
locale.setlocale(locale.LC_ALL, '')

sys.path.append('..') 
from jsreconfig import *

from convert import *
from addids import *
from distributed import *
from PerformanceMeasures import computeAUC
from Fscore import *

def readAUC(source):
    predictions = []
    correct = []
    for line in source:
        line = line.strip().split()
        predictions.append(float(line[2]))
        correct.append(float(line[1]))
    auc = computeAUC(predictions, correct)
    return auc

cvbase = basepath + os.sep + 'CV' + os.sep
splits = cvbase + 'corpus'
trained = cvbase + 'trained'
predict = cvbase + 'predict'
result = cvbase + 'output.sql'

if os.path.exists(trained):
	print >> sys.stderr, 'FATAL: Path ' + trained + ' already exists!'
	sys.exit(1)

if os.path.exists(predict):
	print >> sys.stderr, 'FATAL: Path ' + predict + ' already exists!'
	sys.exit(1)

if os.path.exists(result):
	print >> sys.stderr, 'FATAL: Path ' + result + ' already exists!'
	sys.exit(1)

if not os.path.exists(splits) or os.path.isfile(splits):
	print >> sys.stderr, 'FATAL: Directory ' + splits + ' does not exist!'
	sys.exit(1)

#corpora= os.listdir(splits) #Contains all five corpora
corpora = os.environ["CORPORA"].split()

#Train a Model
print "Step1-Training"
cmd = []
regex = re.compile('\D+\d+')
#w = 2
#n = 3
w = 1
n = 1

for corpus in corpora:
    for train in glob.glob(splits + os.sep + corpus + os.sep + "train*.txt"): #Iterate over Traindata        
        trainName = os.path.basename(train)
        trainName = regex.search(os.path.basename(trainName)).group(0) #For example train[0-9]
        
        dir = trained + os.sep + corpus + os.sep + trainName + os.sep
        os.makedirs(dir)
        start = time.time()
#        for w in range(1,4):
#            for n in range(1,4):
#                print("w=" +str(w) +" n=" +str(n))
#        cmd.append("java -classpath /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/bin/:/vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/lib/* -mx1024M org.itc.irst.tcc.sre.Train -m 512 -k SL -n " +str(n) +" -w " +str(w) +" " +train +" " +dir+"trainn\="+str(n) +"w\=" +str(w) +".model")

        os.chdir(jsre)

        # Kersten: changed command to use newly exported jar file for training with debugged code which really uses window size and n-gram
#        job = subprocess.Popen("java -classpath '" + jsre_classpath + "' -mx8024M org.itc.irst.tcc.sre.Train -m 512 -k SL -n " + str(n) + " -w " + str(w) + " " + train + " " + dir + "trainn\=" + str(n) + "w\=" + str(w) + ".model", shell=True)
        for w in range(1,4):
            for n in range(1,4):
                job = subprocess.Popen("java -jar " + jsre_classpath_train + " -n " + str(n) + " -w " + str(w) + " " + train + " " + dir + "trainn\=" +      str(n) + "w\=" + str(w) + ".model", shell=True)
#                break
        job.wait()
        end = time.time()
#        break
#os.chdir(jsre)
#runDistributed(4, cmd)  



print "Step 2 predict!"
cmd = []
regex = re.compile('(trainn=)(\d+)(w=)(\d)(\.model)')
for corpus in corpora:
    print corpus
    for split in glob.glob(trained + os.sep + corpus + os.sep + "*"):
        split = os.path.basename(split)
        outdir = predict + os.sep + corpus + os.sep + split + os.sep
        os.makedirs(outdir)
        for model in glob.glob(trained + os.sep + corpus + os.sep + split + os.sep + "*.model"):
            n = regex.search(os.path.basename(model)).group(2)
            w = regex.search(os.path.basename(model)).group(4)

            test = splits + os.sep + corpus + os.sep + "test"
#            print("java -classpath /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/bin/:/vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/lib/* -mx1024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")

            cmd.append("java -classpath '" + jsre_classpath + "' -mx2024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")

            os.chdir(jsre)
            job=subprocess.Popen("java -classpath '" + jsre_classpath + "' -mx2024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out",shell=True)
            job.wait()

#os.chdir(jsre)
#runDistributed(4, cmd)



#print "Step 2 predict!"
#cmd = []
#regex = re.compile('(trainn=)(\d+)(w=)(\d)(\.model)')
#for corpus in corpora:
#    print corpus
#    for split in glob.glob(trained + os.sep + corpus + os.sep + "*"):
#        split = os.path.basename(split)
#        outdir = predict + os.sep + corpus + os.sep + split + os.sep
#        os.makedirs(outdir)
#        for model in glob.glob(trained + os.sep + corpus + os.sep + split + os.sep + "*.model"):
#            n = regex.search(os.path.basename(model)).group(2)
#            w = regex.search(os.path.basename(model)).group(4)

#            test = splits + os.sep + corpus + os.sep + "test"
##            print("java -classpath /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/bin/:/vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre-Phil/source/lib/* -mx1024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")
#            # Kersten: not used at all, because runDistributed(4, cmd) is commented out:
##            cmd.append("java -classpath '" + jsre_classpath + "' -mx2024M org.itc.irst.tcc.sre.Predict " +test+split[5:]+".txt"   +" "  +model +" " + outdir +"predictn="+n+"w="+w+".out")
#            # Kersten: changed code to use new jar file for prediction step (so far without multiprocessing
#            os.chdir(jsre)
#            print "############"
#            print jsre_classpath_test
#            print test + split[5:]+".txt"
#            print model
#            print outdir +  "predictn="+n+"w="+w+".out"
#            print "############"
##            sys.exit(0)
#            job=subprocess.Popen("java -jar " + jsre_classpath_test + " " + model + " " + test + split[5:] +".txt" + " " +  outdir +"predictn="+n+"w="+w+".out",shell=True)
#            job.wait()

##os.chdir(jsre)
##runDistributed(4, cmd)


print "Step 3 evaluate!"
cmd = []
regex = re.compile('predictn=(\d+)w=(\d+)\.out')
resultFile = open(result, 'w')
resultFile.write("-- Date created:  " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + "\n\n")
threshold = 0.
for corpus in corpora:
    for split in glob.glob(predict + os.sep + corpus + os.sep + "*"):
        split = os.path.basename(split)
        fold = split[5:]
        print corpus, split
        for prediction in glob.glob(predict + os.sep + corpus + os.sep + split + os.sep + "*.out"):
            resultFile.write("-- BEGIN experiment -- corpus: '" + corpus + "', split: '" + split + "', fold: '" + fold + "', prediction file: '" + prediction + "'\n")
            n = regex.search(os.path.basename(prediction)).group(1)
            w = regex.search(os.path.basename(prediction)).group(2)
            print n,w 
            print "###", prediction
            convert(prediction) #Convert into expected data format

            f = open(prediction)
            # change:
            try:
                auc= readAUC(f)
            except:
                auc = "Null"
#                print "no auc, division by zero", "#####"
            f.close()
            f = open(prediction)
            F, prec, rec, TP, FP, FN, TN = readResults(f, threshold)
            f.close()
#            print auc, F, prec, rec

            # write experiment parameters

            resultFile.write("INSERT INTO ppiCV (parsertype, parser, corpus, fold, kernel, kernel_script) " + 
		 "VALUES ('POS tagger', 'TextPRO (Version06?)', '" + corpus + "', " + fold + ", 'SL', 'jsre; n=" + n + " (n-gram), w=" + w + " (window)');\n")
            
            # write experiment evaluation data
            resultFile.write("UPDATE ppiCV SET tp = " +str(TP) +", fn = " +str(FN) +", tn = " +str(TN) +", fp = " +str(FP) +", total = " +str(TP+TN+FP+FN) +", auc = " + str(auc) + " , precision_ = " + str(prec) + " , recall = " + str(rec) + ", f_measure = " + str(F) + " WHERE ppiCVid = currval('ppiCV_ppiCVid_seq');\n")

            # write single predictions
            test = splits + os.sep + corpus + os.sep + 'test' + fold + '.txt' # same as in Step 2 predict
            addids(prediction, test) # Replace sequence number with original pair IDs from
            f = open(prediction)
            for line in f:
                line = line.split()
                # example line: "9 1.0 0.586770226173"
                if float(line[2]) >= threshold:
                    insertString = '1'
                else:
                    insertString = '0'
                
                resultFile.write("INSERT INTO ppiCVoutput (expId, pair, output, prediction) VALUES (currval('ppiCV_ppiCVid_seq'), '" + line[0] + "', '" + insertString + "', " + line[2] + ");\n")
            f.close() 

            resultFile.write("-- END experiment\n\n")

resultFile.close


