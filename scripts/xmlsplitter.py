#  Ammar Qaseem
import sys
import gzip
import os
import xml.etree.ElementTree as ET
from optparse import OptionParser

def splitting(corpus):



    cmd = "mkdir corpus/"+ corpus + os.sep + corpus + os.sep
    os.system(cmd)

    print "splitting..."
    test_file = "corpus/"+ corpus +"/test0.txt.gz"
    context = ET.iterparse(gzip.open(test_file), events=('end', ))
    index = -1
    j = 0
    max_lim = 10000
    f = gzip.GzipFile("corpus/"+ corpus + os.sep + corpus + os.sep +"test" + str(j) + ".txt.gz", 'wb')
    #gzip.GzipFile(options.output,'w') 
    for event, elem in context:
        if elem.tag == 'document':
            index += 1
            #print "doc", index
            sys.stdout.write("Documents progressed: %d\r" % index )
            sys.stdout.flush()
            
            if (index == (max_lim*j)):
                f.write("</corpus>")
                f.close()    
                f = gzip.GzipFile("corpus/"+ corpus + os.sep + corpus + os.sep +"test" + str(j) + ".txt.gz", 'wb')
                #print "file", j
                j=j+1
                
                header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><corpus source=\""+ corpus +"\">\n"
                f.write(header)
                #with open(filename, 'wb') as f:
            if (index < (max_lim*j)):   
                #print "writing :", index
                #print f 
                f.write(ET.tostring(elem))
                elem.clear()    
                
                #f.write("</corpus>")
                
    f.write("</corpus>")            
    f.close()

                  
    sys.stdout.write("\n")



if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus") 

    (options, args) = parser.parse_args()
    

    try:
        
        splitting(options.corpus)

    except:
        pass
