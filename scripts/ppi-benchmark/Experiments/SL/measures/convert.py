#/bin/python

import sys
def signum(int):
    if(int <= 0):
        return -1;
    elif(int > 0):
        return 1;


def convert(file):
    f = open(file)
    reverse=-1;
    for line in f:
        line = line.split()
        predictClass = int(float(line[0]))
        predict = float(line[1])
        classification = int(float(line[2]))
        #    print str(predictClass) +"\t" +str(predict) +"\t" +str(classification)
        if(predict <0.0 and predictClass==1 or predict >0.0 and predictClass==0):
            reverse=1;
        else:
            reverse=0;
    f.close()


    f = open(file)
    i=0;
    array= []
    for line in f:
        line = line.split()
        predictClass = float(line[0])
        predict = float(line[1])
        classification = float(line[2])
        if(classification==0):
            classification=-1
        if(reverse==0):
            i=i+1
            array.append(str(i)+ " " +str(classification) +" " +str(predict))
            #        print str(i)+ " " +str(classification) +" " +str(predict)
        else:
            i=i+1
            array.append(str(i)+ " " +str(classification) +" " +str(0-predict))
            #        print str(i)+ " " +str(classification) +" " +str(0-predict)

    f.close()

    f = open(file, 'w')
    while(len(array)>0):
        f.write(array.pop(0) +"\n")

