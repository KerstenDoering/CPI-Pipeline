#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# Kersten Doering 11.02.2015

# this script reads identifiers from DS1.xml-ptb-s.txt and adds them to DS1.xml-ptb-s.txt-parsed.txt with tab separation
# otherwise the programme of step 3 in the PPI preprocessing pipeline will not recognize the input sentences from Charniak-Johnson parser (step 2)

from optparse import OptionParser


def run_merg_identifier(corpus):

    # get tags
    tags = []
    _filename_tags = corpus + '.xml-ptb-s.txt'
    
    
    infile_tags = open(_filename_tags,"r")
    for line in infile_tags:
        # a line looks like this:
        # <s DS1.d0.s0> Bestrophin-1  enables Ca2+-activated Cl-conductance in epithelia. </s>
        # whitespace splitting and removing of closing tag of the text element
        tag = line.strip().split(" ")[1][:-1]
        tags.append(tag)
    infile_tags.close()

    # add tags to sentences in Charniak-Johnson format (order is the same)
    _filename_parsed = corpus + '.xml-ptb-s.txt-parsed.txt'
    infile_parsed = open(_filename_parsed,"r")

    # save modified version
    _filename_out = corpus + '.xml-ptb-s.txt-parsed_modified.txt'
    outfile = open(_filename_out,"w")
    for index,line in enumerate(infile_parsed):
        outfile.write(tags[index]+"\t"+line)
    infile_parsed.close()
    outfile.close()

    print "merge is done...\n"


if __name__ == "__main__":
    

    parser = OptionParser()

    parser.add_option("-c", "--corpus", dest="corpus",
                      default=None,
                      help="specify the corpus") 

    (options, args) = parser.parse_args()

        
    run_merg_identifier(options.corpus)


