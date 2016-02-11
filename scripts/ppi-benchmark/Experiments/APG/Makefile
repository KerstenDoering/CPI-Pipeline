include ../../Makefile.config

# Contained in the Pyysalo bechmark corpora
#TOKENIZER=split
#PARSER=split-parse

# Produced by the pipeline
TOKENIZER=Charniak-Lease
PARSER=Charniak-Johnson-McClosky

# Contained in the Pyysalo bechmark corpora
#TOKENIZER=Charniak-Lease
#PARSER=Charniak-Lease


PYTHON=/usr/bin/python

apg-CV:
	echo -n $(foreach c,${Corpora},\
		$(shell echo -n $(MAKE) apg-CV-core CORPUS="$c" '@')) \
		| $(XARGSquiet) -d '@' --max-args 1 --max-procs 1 bash -c

apg-CV-core: ${APGdata}/CV
	@test -d "${APGdata}/CV/corpus/${CORPUS}" || \
		$(MAKE) err MSG="Directory '${APGdata}/CV/corpus/${CORPUS}' does not exist (check variable CORPORA and re-run 'cd ${APGdata} && make clean all')."
	cd CV && \
		rm -rf corpus && \
		rm -rf dictionary/ linearized/ normalized/ predict/ trained/ && \
		mkdir corpus && \
		ln -sfT "${APGdata}/CV/corpus/${CORPUS}" "./corpus/${CORPUS}" && \
		nice bash -c "TOKENIZER='${TOKENIZER}' PARSER='${PARSER}' $(PYTHON) run.py" && \
		rm -rf test*.txt train*.txt
#	cd CV && \
		rm -rf predict/ trained/ && \
		mkdir corpus && \
		nice bash -c "TOKENIZER='${TOKENIZER}' PARSER='${PARSER}' $(PYTHON) run.py" && \
		rm -rf test*.txt train*.txt

apg-CC: apg-CC-core
	
apg-CC-core: ${APGdata}/CC
	@test -d "$<" || $(MAKE) err MSG="Directory '$<' does not exist."
	$(MAKE) check-corpus-directories \
		DIRECTORIES="$(shell find "$</" -maxdepth 1 -mindepth 1 -type d | xargs --max-args 1 basename | xargs echo)"
	cd CC && \
		rm -rf corpus/ && \
		rm -rf dictionary/ linearized/ normalized/ predict/ trained/ && \
		mkdir corpus && \
		ln -sf --target-directory ./corpus/ $</* && \
		nice bash -c "TOKENIZER='${TOKENIZER}' PARSER='${PARSER}' $(PYTHON) run.py"

#		rm -rf corpus/ linearized/ normalized/ predict/ trained/ && \
#		ln -sf ${APGdata}/CC/corpus ./corpus && \
#		python run.py

apg-CL: apg-CL-core

apg-CL-core: ${APGdata}/CL
	@test -d "$<" || $(MAKE) err MSG="Directory '${APGdata}/CL' does not exist."
	$(MAKE) check-corpus-directories \
		DIRECTORIES="$(shell find "$<" -maxdepth 1 -mindepth 1 -type d | xargs --max-args 1 basename | xargs echo)"
	cd CL && \
		rm -rf corpus dictionary/ linearized/ normalized/ predict/ trained/ && \
		mkdir -p corpus && \
		ln -sf --target-directory corpus $</* && \
		nice bash -c "TOKENIZER='${TOKENIZER}' PARSER='${PARSER}' $(PYTHON) run.py"
	

${APGdata}/CV ${APGdata}/CC ${APGdata}/CL:
	cd ${APGdata}  && $(MAKE) "$@"


check-corpus-directories:
ifndef DIRECTORIES
	$(error Variable DIRECTORIES undefined.)
else
ifneq ($(filter-out $(DIRECTORIES),$(CORPORA)),)
	$(error Some corpora [$(filter-out $(DIRECTORIES),$(CORPORA))] have not yet been preprocessed (chek variable CORPORA and re-run 'cd ${APGdata} && make clean all') )
endif
ifneq ($(filter-out $(CORPORA),$(DIRECTORIES)),)
	$(warning Some corpora have been preprocessed [$(filter-out $(CORPORA),$(DIRECTORIES))] and cannot be ignored, this is a limitation. (You may chek variable CORPORA and re-run 'cd ${APGdata} && make clean all') )
endif
endif

