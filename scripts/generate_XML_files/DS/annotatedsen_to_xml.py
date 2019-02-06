#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2015, Elham Abbasian <e_abbasian@yahoo.com>, Kersten Doering <kersten.doering@gmail.com>
    This parser reads annotated sentences (output from get_relations.py) in a tab-separated format to generate a unified XML format (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).
"""

# module to make use of regular expressions
import re

# set the default encoding to utf8 and ignore all decoding/encoding steps.
# (ToDo: check whether the encoding command is needed - debug)
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# optparse - Parser for command-line options
from optparse import OptionParser

# import this function to add quotation arround the input text and ignore the extra quotations inside the sentence text
#from xml.sax.saxutils import escape # (ToDo: not needed - debug)
from xml.sax.saxutils import quoteattr

### MAIN PART OF THE SCRIPT ###
if __name__=="__main__":
    # configure parsing of command-line arguments
    parser= OptionParser()
    parser.add_option("-i", "--input", dest="i", help='name of the input file',default="training_dataset_sorted.csv")
    parser.add_option("-o", "--output", dest="o", help='name of the output file',default="DS.xml")
    (options,args)=parser.parse_args()
    # save parameters in an extra variable
    input_file= options.i
    output_file = options.o
    # open input file with annotated sentences
    infile = open(input_file,"r")
    # open output file
    outfile = open(output_file,"w")

    #example for the input format:
    #18227838-359	The mood stabilizers <compound-id="28486,3028194">lithium</compound-id> and <compound-id="3121">valproate</compound-id>  activate the <protein-id="P29323">ERK</protein-id> pathway in prefrontal cortex and hippocampus and potentiate <protein-id="P29323">ERK</protein-id> pathway-mediated neurite growth, neuronal survival and hippocampal neurogenesis.	lithium__ERK__no_interaction	valproate__ERK__interaction

    #example for the output format
    """
    <?xml version="1.0" encoding="UTF-8">
    <corpus source="DS">
      <document id="DS.d0" origId="18227838">
        <sentence id="DS.d0.s0" origId="18227838-359" text="The mood stabilizers lithium and valproate activate the ERK pathway in prefrontal cortex and hippocampus and potentiate ERK pathway-mediated neurite growth, neuronal survival and hippocampal neurogenesis."/>
            <entity id="DS.d0.s0.e0" origId="28486,3028194" charOffset="x1-y1" type="compound" text="lithium"/>
            <entity id="DS.d0.s0.e1" origId="3121" charOffset="x2-y2" type="compound" text="valproate"/>
            <entity id="DS.d0.s0.e2" origId="P29323" charOffset="x3-y3" type="protein" text="ERK"/>
            <interaction id="DS.d0.s0.i0" e1="DS.do.s0.e0" e2="DS.do.s0.e2" type="no_interaction" directed="False" />
            <interaction id="DS.d0.s0.i1" e1="DS.do.s0.e1" e2="DS.do.s0.e2" type="interaction" directed="False" />
        </sentence>
        [...]
      </document>
      [...]
    </corpus>
    """

    # add XML header and define corpus source
    outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+"\n")
    outfile.write("<corpus source=\"DS\">"+"\n")

    # variable to store and compare the last read PubMed ID to notice whether there are multiple sentences with the same PubMed ID or not
    # the document ID refers to the PubMed ID (origID)
    pre_pmid=""

    # doc_num counts the number of created documents
    doc_num =0
    count = 0
    # read lines in CSV file
    for line in infile :
        # tab-separated format
        temp = line.strip().split("\t")
        # get PubMed ID, sentences ID, and the sentence itself
        # (ToDo: use a split command instead of this regular expression - debug)
        #curr_pmid = re.match('(\d{8})',temp[0]).group(0)
        curr_pmid = re.match('(\d+)',temp[0]).group(0)
        count+=1
        sys.stdout.write("Sentences progressed: %d\r" % count )
        sys.stdout.flush() 
        #print count
        pmid_sent_num = temp[0]
        sentence_text = temp[1]
        # find all annotated proteins and compounds by matching their tags
        pro_positions=  [(a.start(), a.end()) for a in list(re.finditer('<protein-id="(.*?)">(.*?)</protein-id>',sentence_text))]
        cmp_positions =  [(a.start(), a.end()) for a in list(re.finditer('<compound-id="(.*?)">(.*?)</compound-id>',sentence_text))]
        # join the two lists
        positions = pro_positions + cmp_positions
        positions.sort()
        #Initialize the list with the number of identified tags
        entity_list =[]
        entity_list=[0]*len(positions)
        # iterate over all identified positions of the identified tags
        for i in range(len(positions)):
            # initialze the second dimension of the list with a length of four (entity_type,entity_id,entity_text,entity_charoffset)
            entity_list[i]=[0]*4
            # store these four elements with grouping in the regular expression
            obj = re.match('<(protein|compound)-id="(.*?)">(.*?)</(protein-id|compound-id)>',sentence_text[positions[i][0]:positions[i][1]])
            entity_list[i][0]=obj.group(1) #entity_type
            entity_list[i][1]=obj.group(2) #entity_id
            entity_list[i][2]=obj.group(3) #entity_text
            entity_list[i][2]=entity_list[i][2].replace("[","(").replace("]",")")
            # the entity_charoffset will be assign later after having the pure sentence text generated (without any tags)

        # the sentence without any tags will be generated by deleting all tags via text concatenation
        # initialize (ToDo: initialization like this not needed - debug)
        pur_sent_text = sentence_text
        # enumerate over the list of positions (index, value)
        for i,e in reversed(list(enumerate(positions))):
            pur_sent_text = pur_sent_text[0:positions[i][0]]+entity_list[i][2]+pur_sent_text[positions[i][1]:]

        # get the character offset of all identified synonyms
        # decode the sentences to UTF8 to prevent the usage of more than one character for special letters, symbols, etc.
        # make use of a list of repeated synonyms and synonym positions
        repeated_syn_pos =[]
        rep_syn =[]
        for i in range(len(entity_list)) :
            # check whether this is the fist occurrence of the current synonym
            if not entity_list[i][2] in rep_syn :
                # get the list of positions of all occurences of the current synonym
                u_pur_sent_text = pur_sent_text.decode("utf8")
                charoffset_value = [(a.start(), a.end()) for a in list(re.finditer(re.escape(entity_list[i][2]),u_pur_sent_text))]
                # check whether it occures only once such that the charoffsetone directly be assigned
                if len(charoffset_value) == 1 :
                    entity_list[i][3] = str(charoffset_value[0][0])+"-"+str(charoffset_value[0][1])
                else:
                    # if it occures more than one time, the charoffset has to be assigned according to the first pair of positions
                    entity_list[i][3] = str(charoffset_value[0][0])+"-"+str(charoffset_value[0][1])
                    # append this synonym to the rep_syn list to store all repeated synonyms in this sentence
                    rep_syn.append(entity_list[i][2])
                    # delete the fist pair of positions from the list
                    charoffset_value = charoffset_value[1:]
                    # add the rest of positions pairs for the current synonym to another list
                    for j in range(len(charoffset_value)):
                        repeated_syn_pos.append([entity_list[i][2],charoffset_value[j][0],charoffset_value[j][1]]) 
            else:
                # this case refers to at least the second occurrence of the synonym
                # for each repeated synonym, assign the first position pair from the repeated_syn_pos list
                for k in range(len(repeated_syn_pos)):
                    if repeated_syn_pos[k][0] == entity_list[i][2]:
                        break
                entity_list[i][3] = str(repeated_syn_pos[k][1])+"-"+str(repeated_syn_pos[k][2])

        # get pairs and their interaction status (separated by a double underscore)
        listof_int_noint = temp[2:]
        interaction_list=[0]*len(listof_int_noint)
        for i in range(len(listof_int_noint)):
            interaction_list[i]=listof_int_noint[i].split('__')
        # interaction/no_interaction corresponds to True/False
        TF_int_list=[0]*len(interaction_list)
        for intid in range(len(interaction_list)) :
            if interaction_list[intid][2]=="interaction" :
                TF_int_list[intid]="True"
            else :
                TF_int_list[intid]="False"
        # debug:
#        print TF_int_list

        # build XML structure
        # check whether the PubMed ID changed in comparision to the last parsed sentence
        if curr_pmid == pre_pmid :
            # if this is the case, only the sentence ID has to be increased
            sent_num +=1
            
            # add sentence ID using the current document number 
            # (doc_num has to be decreased by one, because this index is automatically increased after each sentence)
            # all openning and closing squared brackets ([,]) should be replaced with round brackets, because they will make problems in the tokenization step of the (preprocessing) pipeline
            pur_sent_text = pur_sent_text.replace("[","(").replace("]",")")

            outfile.write("        <sentence id=\"DS.d"+str(doc_num-1)+".s"+str(sent_num)+"\" origId=\""+str(pmid_sent_num)+"\" text="+quoteattr(pur_sent_text)+">"+"\n")

            # build entity tags according to the list identified tags from the CSV file (entity_list)
            for i in range(0,len(entity_list)) :
                outfile.write("            <entity id=\"DS.d"+str(doc_num-1)+".s"+str(sent_num)+".e"+str(i)+"\" origId=\""+entity_list[i][1]+"\" charOffset=\""+entity_list[i][3]+"\" type=\""+entity_list[i][0]+"\" text="+quoteattr(entity_list[i][2])+"/>"+"\n")

            # insert types of interaction for each pair of entities
            # get the index of the synonym interactions in entity_list
            origId = "DS.d"+str(doc_num-1)+".s"+str(sent_num)
                
            for int_id in range(len(interaction_list)) :
                for ent_id in range(len(entity_list)):
                    if interaction_list[int_id][0] in entity_list[ent_id]:
                        break
                first_entity=ent_id
                for k in range(len(entity_list)):
                    if interaction_list[int_id][1] in entity_list[k]:
                        break
                second_entity=k
                outfile.write("            <pair e1=\""+origId+".e"+str(first_entity)+"\" e2=\""+origId+".e"+str(second_entity)+"\" id=\""+origId+".i"+str(int_id)+"\" interaction=\""+TF_int_list[int_id]+"\" />"+"\n")                
            # close sentence tag
            outfile.write("        </sentence>\n")
        # if the current PubMed ID changed in comparison to the last parsed sentences
        else :
            if not doc_num == 0 :
                outfile.write("    </document>\n")
            sent_num =0
            # a new document tag has to be opened and the sentences can be added
            outfile.write("    <document id=\"DS.d"+str(doc_num)+"\" origId=\""+str(curr_pmid)+"\">"+"\n")
            # replace squared brackets ([,]) with round brackets
            pur_sent_text = pur_sent_text.replace("[","(").replace("]",")")
            outfile.write("        <sentence id=\"DS.d"+str(doc_num)+".s"+str(sent_num)+"\" origId=\""+str(pmid_sent_num)+"\" text="+quoteattr(pur_sent_text)+">"+"\n")
            # now have to make entity tags according to entity_list data.
            for i in range(0,len(entity_list)) :
                outfile.write("            <entity id=\"DS.d"+str(doc_num)+".s"+str(sent_num)+".e"+str(i)+"\" origId=\""+entity_list[i][1]+"\" charOffset=\""+entity_list[i][3]+"\" type=\""+entity_list[i][0]+"\" text="+quoteattr(entity_list[i][2])+"/>"+"\n")
            # build entity tags
            origId = "DS.d"+str(doc_num)+".s"+str(sent_num)
            for int_id in range(len(interaction_list)) :
                for ent_id in range(len(entity_list)):
                    if interaction_list[int_id][0] in entity_list[ent_id]:
                        break
                first_entity=ent_id
                for k in range(len(entity_list)):
                    if interaction_list[int_id][1] in entity_list[k]:
                        break
                second_entity=k
                outfile.write("            <pair e1=\""+origId+".e"+str(first_entity)+"\" e2=\""+origId+".e"+str(second_entity)+"\" id=\""+origId+".i"+str(int_id)+"\" interaction=\""+TF_int_list[int_id]+"\" />"+"\n")
            # close sentence tag
            outfile.write("        </sentence>\n")
            # set new PubMed ID as the last parsed document ID and increase document index
            pre_pmid = curr_pmid
            doc_num+=1

    # close document tag
    outfile.write("</document>\n")
    # close corpus tag
    outfile.write("</corpus>\n")
    # close files
    infile.close()
outfile.close()
sys.stdout.write("\n")
