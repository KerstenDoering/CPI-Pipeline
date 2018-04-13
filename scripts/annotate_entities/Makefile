
#  Copyright (c) 2018, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>

Processors=2 # defaulf


help:
	$(info use 'make annotate \
		InputFile="" \
		OutputFile="" \
		Processors=""')
	@echo
	@echo "Where:"
	@echo "     InputFile   :   The file contains pmids, one pmid per line."
	@echo "     OutputFile  :   The output file, where compound and protein entities are annotated. The file located in annotate_output directory."	
	@echo "     Processors  :   The number of cores used for processing."	



annotate: check_parm call_PubTator run_annotate


call_PubTator: $(InputFile)
	python call_PubTator.py -i $(InputFile) -o PubtatorOut.txt -t BioConcept -f PubTator

	
run_annotate:
	python annotate.py -i PubtatorOut.txt -o $(OutputFile) -p $(Processors)

check_parm:
ifeq ($(InputFile),)
	$(error FATAL ERROR: Variable InputFile undefined.)
endif
ifeq ($(InputFile),)
	$(error FATAL ERROR: Variable InputFile undefined.)
endif


clean:
	@rm -rf PubtatorOut.txt missed_pmids/ done_pmids/ annotate_output/

