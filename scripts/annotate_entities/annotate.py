#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    #  Copyright (c) 2018, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>
    This script To annotate the entities(in our case entities are compound and protein).
"""

import os, sys
import datetime, time
import nltk.data
import gzip
import os.path
import cPickle as pickle
import re # regular expressions


punkt_tokenizer         = nltk.data.load('tokenizers/punkt/english.pickle')
myabbrevs = ['dr', 'vs', 'mr', 'Mrs', 'prof', 'inc', 'i.e', 'e.g', 'et al', 'eq',  'resp']
for abbr in myabbrevs:
    punkt_tokenizer._params.abbrev_types.add(abbr)


DictUniProt = {}

# This fuction to make tokenization for text and split it into sentences
def split_to_sentences(text):
    return punkt_tokenizer.tokenize(text)


# This function create a dictionary (key: GeneID, value: UniProtID).
# Save this a pickle file to use it later.
def UniProt_mapping(idmapping_file):

    _file = gzip.open(idmapping_file, 'rb')

    idtype="GeneID"
    #print "fileName:", self.fileName
    #DBUniProtMapping = ProtmineDB.GenesUniProt()
    
    loop_counter = 0
    for line in _file:
    # strip() deletes leading plus ending spaces, etc.
    # split(delimiter) generates a list out of a string and deletes the "delimiter" (here: tab)
        temp = line.strip().split("\t")
        #print temp[1]
        # Check the second column - if its value equals "GeneID", the required UniProt ID and gene ID is stored in the output file
        # debug:
        # if test_case is True
        if temp[1] == idtype:

            loop_counter = loop_counter +1
            
            geneid = int(temp[2])

            uniprot = temp[0]

            if geneid in DictUniProt:
            
                DictUniProt[geneid] = DictUniProt[geneid] + ',' + uniprot
                
            
            else:

                DictUniProt[geneid] = uniprot
                
      
      # Save the dictionary into pickle file
    pickle.dump( DictUniProt, open( "protmine/uniprot.p", "wb" ) )
    
    
             

# This function receive a text and the list of entities to be annotate with their postions in the text, and return a text with annotated those entities.
def annotating(pmid, text, entities):
    #<compound-id="80654">Cl</compound-id>
    l = list(text)
    l2 = list()
    pos = 0
    for row in entities:
        #print row
        rowTokens = row.split('\t')
        startEnt = int(rowTokens[1])
        endEnt = int(rowTokens[2])
        entity = rowTokens[3]
        entType  = rowTokens[4]
        entID = ''
        if len(rowTokens) > 5 :
            
            if (entType == "Chemical"):
             
                cid   =  rowTokens[5]
                
                entID = cid
                
            elif (entType == "Gene"):
            
                gid = (rowTokens[5].split('(')[0]).split(';')
                
                gg = ''
                for g in gid:
                    
                    #print g
                    try:
                        if int(g) in dict:
                            #print g
                            gg += dict[int(g)] + ","
                    except:
                        continue
                        
                if gg != '':
                    entID = gg[:-1]
                
                
        else:
        
            entID = ''
        
          
        l2 += l[pos:startEnt]
        
        
        if (entType == "Chemical"):
            fullCompAnnotEntity = '<compound-id="'+entID+'">' + str("".join( l[startEnt:endEnt])) + '</compound-id>'
            l2 += fullCompAnnotEntity
        
        elif (entType == "Gene"):
            fullCompAnnotEntity = '<protein-id="'+entID+'">' + str("".join( l[startEnt:endEnt])) + '</protein-id>'
            l2 += fullCompAnnotEntity
                
        
        pos = endEnt
    
    
    l2 += "".join( l[pos:])  
    annotedText = "".join( l2 )
    return annotedText


def getSynonyms(ann_text,tag):
    
    
    tag_start = [(a.start(), a.end()) for a in list(re.finditer('<'+tag+'=\".*?">', ann_text))]
    tag_end = [(a.start(), a.end()) for a in list(re.finditer('</'+tag+'>', ann_text))]
    #comp_tag_end = [(a.start(), a.end()) for a in list(re.finditer('</compound-id>', ann_text))]

    syn_pos=[]
    lstSyn=[]
    
    for elem in tag_start:

        syn_pos.append(elem[1])

    for elem in tag_end:

        syn_pos.append(elem[0])

    
    syn_pos.sort()
    
    
    for i in range(0,(len(syn_pos)/2)):

        syn = ann_text[syn_pos[i*2]:syn_pos[(i*2)+1]]
    
        lstSyn.append(syn)
    
    
    return lstSyn


def get_related_entities(ann_text):

    compound_lstSyn = getSynonyms(ann_text,'compound-id')
    protein_lstSyn = getSynonyms(ann_text,'protein-id')

    # Get the unique list to avoid the duplication
    #sorted(set(x), key=x.index)
    compound_lstSyn_unique = sorted(set(compound_lstSyn), key=compound_lstSyn.index)
    protein_lstSyn_unique = sorted(set(protein_lstSyn), key=protein_lstSyn.index)

    

    # if one of two lists is empty then there is not any relation
    if not compound_lstSyn_unique or  not protein_lstSyn_unique :

            return
    
    cand_relation = ""  # initialize
   
    # go through each compound and make relation to each protein(all with all). The default relation is no_interation
    for comp in compound_lstSyn_unique:

        for prot in protein_lstSyn_unique:

            cand_relation += "\t" + comp + "__" + prot + "__" + "no_interaction"
      

    #return (ann_text+relation)
    return (cand_relation)



# This fuction to analyse the output results from Pubtator for annotate entities. This analysis, extract pmid, a text(Title and Abstract) and the entities with their postions in the text. 
def analysisPubtatorRes(fileName, outputFile):
    
    if os.path.splitext(fileName)[-1] == ".gz":
        InFile = gzip.open(fileName, 'rb')
    else:
        InFile = open(fileName, 'rb')
    
    out= "annotate_output/" + outputFile   
    #outFile = gzip.GzipFile(out, 'wb')
    #outFileCand = gzip.GzipFile('annotate_output/final_sentences_with_candidate.txt.gz', 'wb')
    outFileCand = open(out, 'w')
    outFile = open('annotate_output/out_without_candidate.txt', 'w')
    doc_counter = 0
    entities=list()
    rowDict = {}
    i=0
    s=""
    for line in InFile :
        
        if line.strip():
            if line.strip()[:7] == "[Error]":
                i=0
                s=""
                entities=list()
                rowDict = {}
                continue
            if i in (0,1):
                #print line
                tokens = line.strip().split("|")
                if len(tokens) > 1:
                    if tokens[1] == "a" and tokens[2]:
                        s+= " " + tokens[2]
                        #print s
                    elif tokens[1] == "t" and tokens[2]:
                        #print line
                        pmid = tokens[0]
                        s+= tokens[2]
                i+=1
            else:
                tokens = line.strip().split("\t")
                if len(tokens) > 1:
                    
                    if tokens[4] in ("Gene","Chemical"):
                        #entities.append(line.strip()) 
                        offset_b = int(tokens[1])
                        #print offset_b
                        rowDict[offset_b] = line.strip()
                    
        else:
            '''
            print pmid , "\t", s ,"\n"
            for item in entities:
            
                print item
            
            '''

            for key in sorted(rowDict):
            
                entities.append(rowDict[key])
         
            
            annotatedText = annotating(pmid, s, entities)
            
            annotatesSentences = split_to_sentences(annotatedText.strip())
            
            sentID = 0
            for sent in annotatesSentences:
                 
                cand_entities = get_related_entities(sent)
                if cand_entities:
                
                    fullSentence = pmid + '-' + str(sentID) + '\t' + sent + cand_entities
                    outFileCand.write(fullSentence)
                    outFileCand.write('\n')
                else:
                
                    fullSentence = pmid + '-' + str(sentID) + '\t' + sent
                    
                        
                #print fullSentence
                outFile.write(fullSentence)
                outFile.write('\n')
                sentID += 1
            doc_counter+=1
            print >> sys.stderr, "\rProcessing document " + str(doc_counter),
            i=0
            s=""
            entities=list()
            rowDict = {}
        
        
    print         
    InFile.close()
    outFile.close()
    outFileCand.close()



if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-i", "--input", dest="articles",
                      default='abstracts/1.txt',
                      help="specify the path of the pubTator annotated file (default: abstracts/1.txt)")
    parser.add_option("-o", "--output", dest="output",
                      default='annotate_output//final_sentences.txt.gz',
                      help="specify the path of the output (default: annotate_output//final_sentences.txt.gz)")
                  
    parser.add_option("-p", "--processes",
                      dest="PROCESSES", default=2,
                      help="How many processes should be used. (Default: 2)")
    
    
    (options, args) = parser.parse_args()
    #print options.articles
    
    start = time.asctime()
    print "programme started - " + start
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #WDir = dir_path.split('/')[-1]
    #print os.getcwd()
    #UniProt_mapping('protmine/idmapping.dat.gz')
    print "Upload UniProt ..."
    
    if not os.path.exists('uniprot.p'):
        os.system('gunzip uniprot.p.gz')
    
    dict = pickle.load( open( "uniprot.p", "rb" ) )

    print "Done." 
    '''
    #for key, value in dict.iteritems():
    #    key = key + '#'
    #    print key, value
    x = 1117315
    
    if x in dict:
        print dict[x]
    
    else:
        print 'None'
    sys.exit()
    ''' 
    if not os.path.exists(options.articles):
        print "input file: ", options.articles ," does not exits"
        sys.exit()
        
    if not os.path.exists('annotate_output/'):
        os.makedirs('annotate_output/')
          
    analysisPubtatorRes(options.articles, options.output)
    
        
    end = time.asctime()

    print "programme started - " + start
    print "programme ended - " + end


