#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Copyright (c) 2014, Kersten Doering <kersten.doering@gmail.com>

    This parser reads the documents interactions.txt and no_interactions.txt.
    Furhtermore, the algorithm extracts the information from RM_comments.csv,
    whether an entity belongs to the pairs of interaction partners
    (false positive example or not interacting in a given sentence).
    The output file is training_dataset.txt, containing each sentence with 
    PubMed ID and sentence ID. All HTML (colour) tags are replaced with
    XML tags. The pairs with the status Interaction and No Interaction are given
    at tab-separated after the sentence, separated with a double underscore.
    Protein tags are coloured lightgreen, compounds lightblue, and verbs orange.
"""

# module to make use of regular expressions
import re

# read in the comments - there are fpc (false pos. compounds), fpp (false pos. proteins), nic (not interacting compounds), and nip (not interacting proteins)
fpc = {}
fpp = {}
nic = {}
nip = {}
# store all PubMed IDs with sentence ID from RM_comments.csv in this list
keys = []
# open file
infile = open("RM_comments.csv","r")
# take out all entries (do not strip, otherwise column structure is lost)
for line in infile:
    # first column is the sentence ID, second PubMed ID, third fpc, fourth fpp, fifth nic, and sixth nip
    # split columns
    temp = line.split("\t")
    # debug: check whether there are duplicate lines in RM_comments.csv
    if not temp[1] + "-" + temp[0] in keys:
        keys.append(temp[1] + "-" + temp[0])
        fpc[temp[1] + "-" + temp[0]] = temp[2]
        fpp[temp[1] + "-" + temp[0]] = temp[3]
        #no strip before - needs to be done for last entry in row
        nic[temp[1] + "-" + temp[0]] = temp[4].strip()
        nip[temp[1] + "-" + temp[0]] = temp[5].strip()
    #the else case should never happen
    else:
        print "### exception ###"
# close RM_comments.csv
infile.close()

# debug counter variables for pairs with the status Interaction (line_counter_1) and No Interaction (line_counter_0)
line_counter_0 = 0
line_counter_1 = 0
# store sentences with an interaction
interaction_sentences = []
# open document with sentences containing the status Interaction
infile = open("interactions.txt","r")

# at first, positive and negative training examples are considered - depends on fpc and fpp from RM_comments.csv
# after the line with the command opening no_interactions.txt, only sentences with negative examples are considered
# open output file
outfile = open("training_dataset.txt","w")
# iterate over interactions.txt
for line in infile:
    # store all pairs, except fpc and fpp in this list
    pairs = []
    pairs_Interaction = {}
    pairs_NonInteraction = {}
    # tab-separated format
    temp = line.strip().split("\t")
    sentence = temp[1]
    # extract pmid from index: "PubMed ID-sentence ID"
    pmid = temp[0]
    # preprocessing of false positives - delete enclosed colour tags:
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:(lightblue|orange).*?">(.*?)</mark>', sentence))]
    # sort posititions reversely such that a later iteration step is still consistent with the positions after text concatenation
    positions.sort(reverse=True)
    # positions of protein tags
    positions_prot = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen.*?">(.*?)</mark>', sentence))]
    positions_prot.sort(reverse=True)

    # take care for nested tags, e.g. 18403016-276 - compound tagged enclosed in protein tags:
    # iterate over all tagged positions
    for pos in positions:
        # iterate over positions of proteins (protein tags were introduced before compound tags, such that misplaced compound tags need to be removed)
        for pos_prot in positions_prot:
            # if a pair of protein tags is enclosing another pair of tags (e.g. for a compound), delete these inner tags by the regular expression grouping and text concatenation
            if pos_prot[0] <= pos[0] and pos_prot[1] >= pos[1]:
                # debug:
                #print sentence[pos[0]:pos[1]], pmid
                m = re.match('<mark style="background-color:(lightblue|orange).*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(2)

                sentence = sentence[0:pos[0]] + m + sentence[pos[1]:]
                # iteration for this protein tag can be stopped
                break

    # start parsing of all remaining pairs
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:.*?">(.*?)</mark>', sentence))]
    # use reversed sorting, again
    positions.sort(reverse=True)
    # iterate over all positions of tags
    for pos in positions:
        m = re.match('<mark style="background-color:.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(1)
        # find out whether there are false positives inside the sentence (fpc or fpp) - this is important for the class - negative vs. positive (0 vs. 1)
        # ensure that the considered PubMed ID was also read in the RM_comments.csv file to prevent key errors
        if pmid in keys:
            # check whether the considered entity is inside the false positive dictionaries (fpc and fpp)
            # if this is the case, remove its tags with text concatenation
            if m.lower() in fpc[pmid].lower() or m.lower() in fpp[pmid].lower():
                sentence = sentence[0:pos[0]] + m + sentence[pos[1]:]
            # this code fragment was not yet removed, because an earlier implementation used a replacement of spaces inside the tags
            # if there is no annotation of false positive examples in this sentence, nothing has to be done
            # ToDo: debug and remove this case
            else:
                sentence = sentence[0:pos[0]] + " " + sentence[pos[0]:pos[1]] + " " + sentence[pos[1]:]
        # the same happens in the case of sentences that are not annotated in RM_comments.csv, because there will be no (annotated) false positive examples
        else:
            sentence = sentence[0:pos[0]] + " " + sentence[pos[0]:pos[1]] + " " + sentence[pos[1]:]

    # get compound tag positions
    positions_comp = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightblue.*?">(.*?)</mark>', sentence))]
    # sort positions reversely
    positions_comp.sort(reverse=True)
    # get protein tag positions
    positions_prot = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen.*?">(.*?)</mark>', sentence))]
    # sort them reversely
    positions_prot.sort(reverse=True)
    # check and store all pairs with the status Interaction and No Interaction
    for pos_comp in positions_comp:
        # flag for each pair which is potentially in a functional relationship
        # default initialization with True
        c_interaction = True
        # get compound term
        m_comp = re.match('<mark style="background-color:lightblue.*?">(.*?)</mark>',sentence[pos_comp[0]:pos_comp[1]]).group(1)
        # check whether this compound was annotated as non-interacting
        if pmid in keys:
            if m_comp.lower() in nic[pmid].lower():
                c_interaction = False
        # if there are no more protein positions left in the following for-loop, the next compound will be considered
        # if this compound was annotated in RM_comments as non-interacting, the status of the variable interaction is set to False, otherwise the default value True will be assigned
        # this value of interaction can still be set to False from an annotation in the nip dictionary from RM_comments.csv
        # get the protein term the same way the compound term was extracted (regular expression)
        for pos_prot in positions_prot:
            interaction = c_interaction
            m_prot = re.match('<mark style="background-color:lightgreen.*?">(.*?)</mark>',sentence[pos_prot[0]:pos_prot[1]]).group(1)
            if pmid in keys:
                if m_prot.lower() in nip[pmid].lower():
                    interaction = False
            # concatenate compound and protein term with a double underscore (case sensitive)
            pair = m_comp+"__"+m_prot
            # if it is an interacting pair, add the status with another double underscore
            if interaction:
                pairs.append(pair+"__interaction")
                pairs_Interaction[pair] = 1
            # else case
            if not interaction:
                pairs.append(pair+"__no_interaction")
                pairs_NonInteraction[pair] = 0

    # store the sentence text in the variable new_sentence
    new_sentence = sentence
    # remove verb tags (orange) and Gene Ontology terms (yellow)
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:(yellow|orange);.*?">(.*?)</mark>', sentence))]
    # sort positions reversly, again
    positions.sort(reverse=True)
    parts = []
    # iterate over all positions of this type
    for pos in positions:
        m = re.match('<mark style="background-color:(yellow|orange);.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(2)
        # text concatenation of the old sentence for parts before the currently considered position and the newly replaced parts after this position
        new_sentence = sentence[0:pos[0]] + m + new_sentence[pos[1]:]
    # try to remove spaces - error in the Whatizit parser implemented by another developer- not fixed - rearranged positions are OK in most cases
    new_sentence = new_sentence.replace("  "," ").replace(" ,",",").replace(" .",".").replace(" 's","'s").replace(" /","/").replace("/ ","/").replace("( ","(").replace(" )",")").replace(" -","-").replace("- ","-").replace("[ ","[").replace(" ]","]").replace(" +","+").replace("-and", "- and").replace("-over", "- over").strip()
    # replace the original sentence with the newly manipulated text
    sentence = new_sentence
    # get compound postions to replace HTML tags with XML tags
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightblue;.*?">(.*?)</mark>', sentence))]
    # sort positions reversely
    positions.sort(reverse=True)
    for pos in positions:
        # get pair of tags with enclosed compound term
        m = re.match('<mark style="background-color:lightblue;.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(0) 
        # replace the HTML tags with XML tags in the given frame
        new_sentence = sentence[0:pos[0]] + m.replace("mark","compound-id").replace(" style=\"background-color:lightblue;\" id","").replace("> ",">") + new_sentence[pos[1]:]
    # replace the last sentence version with the newly manipulated text, again
    sentence = new_sentence
    # repeat the replacement procedure with protein terms
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen;.*?">(.*?)</mark>', sentence))]
    # sort positions reversely
    positions.sort(reverse=True)
    # iteration over all protein postions
    for pos in positions:
        # get pair of tags with enclosed compound term
        m = re.match('<mark style="background-color:lightgreen;.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(0) 
        # replace the HTML tags with XML tags in the given frame
        new_sentence = sentence[0:pos[0]] + m.replace("mark","protein-id").replace(" style=\"background-color:lightgreen;\" id","") + new_sentence[pos[1]:]

    # replace double spaces created by the rearranged spaces
    new_sentence = new_sentence.replace("  "," ")
    # make list of pairs unique
    pairs = list(set(pairs))
    # it could happen that there are no more pairs after the described removements
    if not len(pairs) == 0:
        # generate the tab-separated structure for the given sentence ant its pairs of compounds and proteins
        outfile.write(temp[0] + "\t" + new_sentence + "\t" + "\t".join(pairs) + "\n")
        # store processed PubMed ID in the list interaction sentences
        # in many cases, there are different sentences referring to the same PubMed ID
        if not temp[0] in interaction_sentences:
            interaction_sentences.append(temp[0])

	line_counter_1 += len(pairs_Interaction)
    line_counter_0 += len(pairs_NonInteraction)

# debug number of interacting pairs (line_counter_1):
print "total lines 0:"
print line_counter_0
print "total lines 1:"
print line_counter_1
# close input file interactions.txt
infile.close()

### repeat the whole procedure for the input file no_interactions.txt ###
# in this file, there are only pairs with the status No Interaction (and False positive example as annotated in RM_comments.csv)
line_counter_0 = 0
line_counter_1 = 0
# list of processed sentences from this input file
no_interaction_sentences =[]
# open input file
infile = open("no_interactions.txt","r")
# start iteration
for line in infile:
    pairs = []
    pairs_Interaction = {}
    pairs_NonInteraction = {}
    # tab-separated format
    temp = line.strip().split("\t")
    # sentence ID
    sentence = temp[1]
    # PubMed ID
    pmid = temp[0]#.split("-")[0]
    # preprocessing of nested tags - delete enclosed colour tags
    # get compound postions
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:(lightblue|orange).*?">(.*?)</mark>', sentence))]
    # sort reversely
    positions.sort(reverse=True)
    # get protein positions
    positions_prot = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen.*?">(.*?)</mark>', sentence))]
    # sort reversely
    positions_prot.sort(reverse=True)
    #example for nested tagging - 18403016-276 - compound tagged enclosed in protein tags (compare comments for the code referring to interactions.txt)
    for pos in positions:
        for pos_prot in positions_prot:
            if pos_prot[0] <= pos[0] and pos_prot[1] >= pos[1]:
                m = re.match('<mark style="background-color:(lightblue|orange).*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(2)
                sentence = sentence[0:pos[0]] + m + sentence[pos[1]:]
                break

    # start parsing of all remaining pairs
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:.*?">(.*?)</mark>', sentence))]
    positions.sort(reverse=True)
    for pos in positions:
        m = re.match('<mark style="background-color:.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(1)
        # check annotation in RM_comments.csv
        if pmid in keys:
            if m.lower() in fpc[pmid].lower() or m.lower() in fpp[pmid].lower():
                sentence = sentence[0:pos[0]] + m + sentence[pos[1]:]
            # compare comments for the code referring to interactions.txt
            else:
                sentence = sentence[0:pos[0]] + " " + sentence[pos[0]:pos[1]] + " " + sentence[pos[1]:]
        else:
            sentence = sentence[0:pos[0]] + " " + sentence[pos[0]:pos[1]] + " " + sentence[pos[1]:]

    # get compound and protein terms which are not annotated in fpc or fpp and add their status interaction or no_interaction
    # compare comments for the code referring to interactions.txt
    # protein positions
    positions_comp = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightblue.*?">(.*?)</mark>', sentence))]
    positions_comp.sort(reverse=True)
    positions_prot = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen.*?">(.*?)</mark>', sentence))]
    positions_prot.sort(reverse=True)
    # compound postions
    for pos_comp in positions_comp:
        c_interaction = False
        m_comp = re.match('<mark style="background-color:lightblue.*?">(.*?)</mark>',sentence[pos_comp[0]:pos_comp[1]]).group(1)
        if pmid in keys:
            if m_comp.lower() in nic[pmid].lower():
                c_interaction = False
        for pos_prot in positions_prot:
            interaction = c_interaction
            m_prot = re.match('<mark style="background-color:lightgreen.*?">(.*?)</mark>',sentence[pos_prot[0]:pos_prot[1]]).group(1)
            if pmid in keys:
                if m_prot.lower() in nip[pmid].lower():
                    interaction = False
            # concatenate currently considered pair
            pair = m_comp+"__"+m_prot
            # interacting pair
            if interaction:
                pairs.append(pair+"__interaction")
                pairs_Interaction[pair] = 1

            # non-interacting pair
            if not interaction:
                pairs.append(pair+"__no_interaction")
                pairs_NonInteraction[pair] = 0

    # remove verb tags (orange) and Gene Ontology terms (yellow)
    new_sentence = sentence
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:(yellow|orange);.*?">(.*?)</mark>', sentence))]
    positions.sort(reverse=True)
    for pos in positions:
        m = re.match('<mark style="background-color:(yellow|orange);.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(2)
        new_sentence = sentence[0:pos[0]] + m + new_sentence[pos[1]:]
    new_sentence = new_sentence.replace("  "," ").replace(" ,",",").replace(" .",".").replace(" 's","'s").replace(" /","/").replace("/ ","/").replace("( ","(").replace(" )",")").replace(" -","-").replace("- ","-").replace("[ ","[").replace(" ]","]").replace(" +","+").replace("-and", "- and").replace("-over", "- over").strip()

    # get compound postions to replace HTML tags with XML tags
    sentence = new_sentence
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightblue;.*?">(.*?)</mark>', sentence))]
    positions.sort(reverse=True)
    for pos in positions:
        m = re.match('<mark style="background-color:lightblue;.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(0) 
        new_sentence = sentence[0:pos[0]] + m.replace("mark","compound-id").replace(" style=\"background-color:lightblue;\" id","").replace("> ",">") + new_sentence[pos[1]:]

    # get protein postions to replace HTML tags with XML tags
    sentence = new_sentence
    positions = [(a.start(), a.end()) for a in list(re.finditer('<mark style="background-color:lightgreen;.*?">(.*?)</mark>', sentence))]
    positions.sort(reverse=True)
    for pos in positions:
        m = re.match('<mark style="background-color:lightgreen;.*?">(.*?)</mark>',sentence[pos[0]:pos[1]]).group(0) 
        parts.append(m + sentence[pos[1]:])
        new_sentence = sentence[0:pos[0]] + m.replace("mark","protein-id").replace(" style=\"background-color:lightgreen;\" id","") + new_sentence[pos[1]:]

    # replace double spaces created by the rearranged spaces
    new_sentence = new_sentence.replace("  "," ")
    # make list of pairs unique and store them in the output file
    pairs = list(set(pairs))
    if not len(pairs) == 0:
        outfile.write(temp[0] + "\t" + new_sentence + "\t" + "\t".join(pairs) + "\n")
        if not temp[0] in no_interaction_sentences:
            no_interaction_sentences.append(temp[0])

	line_counter_1 += len(pairs_Interaction)
    line_counter_0 += len(pairs_NonInteraction)

# debug:
print "total lines 0:"
print line_counter_0
print "total lines 1:"
print line_counter_1

# close input file
infile.close()
# close output file
outfile.close()
# debug:
print "amount of used sentences in interaction.txt: " + str(len(interaction_sentences))
print "amount of used sentences in no_interaction.txt: " + str(len(no_interaction_sentences))

