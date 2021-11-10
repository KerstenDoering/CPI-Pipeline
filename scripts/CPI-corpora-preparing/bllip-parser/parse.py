#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Ammar

import subprocess
import os
import time
from multiprocessing import Pool
from functools import partial
from optparse import OptionParser
import os.path
import re
from bllipparser import RerankingParser

# This function to perform the parsing process to build a syntactic tree
def parseIt(_infile, _outfile):


	#rrp = RerankingParser.from_unified_model_dir('/home/ammar/.local/share/bllipparser/GENIA+PubMed')
	rrp = RerankingParser.fetch_and_load('GENIA+PubMed', verbose=False)
	##rrp = RerankingParser.fetch_and_load('WSJ-with-AUX', verbose=True)

	#print 'Start...'
	#print(rrp.simple_parse('This is simple.'))
	#nbest_list = rrp.parse('This is a sentence.')
	#print(nbest_list)

	INFile = open(_infile, 'r')
	OUTFile = open(_outfile, 'w')
   
	for line in INFile:
		
		obj = re.findall(r'<s.*?>(.*?)</s>',line)
		
		sentence = obj[0].strip()
		#tokens = nltk.word_tokenize(sentence)
		#print(tokens)
		#tagged = nltk.pos_tag(tokens)
		#entities = nltk.chunk.ne_chunk(tagged)
		#print("Ent:", entities)
		#text = nltk.Text(entities)
		#text = entities
		#print('text:', text)
		#for l in entities:
		#    for s in l:
		#        print(entities.Text())
		#print(rrp.simple_parse(sentence))
		##s = rrp.simple_parse(sentence)
		#print 'nbest_list', len(nbest_list)
		#print 'nbest_list', nbest_list
		try:
			nbest_list = rrp.parse(sentence)
			s = str(nbest_list[0].ptb_parse)
			OUTFile.write(s)
			OUTFile.write('\n')
		except:
			print 'Error : ', line
			OUTFile.write('\n')
			continue		

	INFile.close()
	OUTFile.close()


if __name__ == "__main__":
    
		parser = OptionParser()

		parser.add_option("-i", "--input", dest="input", 
		                  default=None,
		                  help="specify the path of the intput file")  
		parser.add_option("-o", "--output", dest="output",
		                  default=None,
		                  help="specify the path of the output file")
		
		
		(options, args) = parser.parse_args()
		 
		parseIt(options.input, options.output)

  

