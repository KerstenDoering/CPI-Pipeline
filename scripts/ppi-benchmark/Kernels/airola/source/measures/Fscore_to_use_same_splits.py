import sys

def F1(TP, FP, FN):
    if (TP == 0. and (FP == 0. or FN == 0.)):
        F = 0.
        prec = 0
        rec = 0
    else:
        prec = float(TP) / float(TP+FP)
        rec = float(TP) / float(TP + FN)
        if (prec == 0 and rec == 0):
            F = 0.
        else:
            F = (2.*prec*rec)/(prec+rec)
    return F, prec, rec

def readResults(outputfile, threshold):
    TP = 0
    FP = 0
    FN = 0
    for line in outputfile:
        line = line.split()
        entity_id=line[0]
        print entity_id
        if(int(entity_id.split('.')[1][1:])<830):
            #print entity_id.split('.')[1][1:]
            continue	
        correct = float(line[1])
        predict = float(line[2])
        if predict <threshold:
            predict = -1.0
        else:
            predict = 1.0
        if predict == 1.0:
            if correct == 1.0:
                TP +=1
            elif correct == -1.0:
                FP += 1
            else:
                print "Fatal error"
                sys.exit(0)
        elif predict == -1.0:
            if correct == 1.0:
                FN += 1
            elif correct == -1.0:
                pass
            else:
                print "Fatal error"
                sys.exit(0)
        else:
            print "Fatal error"
            sys.exit(0)
    F, prec, rec = F1(TP, FP, FN)
    return F, prec, rec

def getAbsoluteNumbers(outputfile, threshold):
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for line in outputfile:
        line = line.split()
        entity_id=line[0]
        print entity_id
        if(int(entity_id.split('.')[1][1:])<830):
            #print entity_id.split('.')[1][1:]
            continue	
        correct = float(line[1])
        predict = float(line[2])
        if predict <threshold:
            predict = -1.0
        else:
            predict = 1.0

        if predict == 1.0:
            if correct == 1.0:
                TP +=1
            elif correct == -1.0:
                FP += 1
            else:
                print "Fatal error"
                sys.exit(0)
        elif predict == -1.0:
            if correct == 1.0:
                FN += 1
            elif correct == -1.0:
                TN += 1
            else:
                print "Fatal error"
                sys.exit(0)
        else:
            print "Fatal error"
            sys.exit(0)

    return TP,FP,FN,TN
