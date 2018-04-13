include ../../Makefile.config

#jsre:
#	$(foreach c,${Corpora},$(MAKE) jsre-core CORPUS=$c expType=$(expType))

jsreBase=${jsreDir}/source
jsreJar=${jsreBase}/dist/xjsre.jar

#not sure how this should be setup
TRAIN_FILES=must.be.defined.to.work
TEST_FILES=must.be.defined.to.work


jsre-core: JSRE_CLASSPATH="${jsreJar}${SEP}${jsreBase}/lib/*"
jsre-core: ${jsreJar}
	$(MAKE) check-expType EXPTYPE=${expType}
	rm -rf ${expType}/corpus ${expType}/predict ${expType}/trained ${expType}/output.sql
	$(MAKE) $(foreach c,$(CORPORA),${expType}/corpus/${c})
	cd ${expType} \
		&& bash -c "baseDir='$(baseDir)' CORPORA='$(CORPORA)' python run.py '${expType}'"

jsre-split: JSRE_CLASSPATH="${jsreJar}${SEP}${jsreBase}/lib/*
jsre-split: expType=split
jsre-split: ${jsreJar}
ifndef TRAIN_FILES
	$(error FATAL ERROR: Variable TRAIN_FILES undefined.)
endif
ifndef TEST_FILES
	$(error FATAL ERROR: Variable TEST_FILES undefined.)
endif
	@echo Cleaning up previous experiment...
	rm -rf ${expType}/corpus ${expType}/predict ${expType}/trained ${expType}/output.sql
	@echo Running experiment...
	cd ${expType} \
		&& time bash -c "baseDir='$(baseDir)' JAVA='$(JAVA) $(MEM2)' NUM_PROCS='$(numberofprocs)' TRAIN_FILES='$(foreach f,${TRAIN_FILES},$(shell readlink -f $f))'  TEST_FILES='$(foreach f,${TEST_FILES},$(shell readlink -f $f))' python run.py '${expType}'" > "$@.log" 2>&1

dummy:
	$(foreach f,${TRAIN_FILES},$f)
	#echo "$(foreach f,${TRAIN_FILES},$(shell readlink -f $f))"

${SLdata}/CV/corpus/%:
	cd ${corpusDir} && $(MAKE) $@ 

${SLdata}/PR/corpus/%:
	cd ${corpusDir} && $(MAKE) $@ 

${SLdata}/XX/corpus/%:
	cd ${corpusDir} && $(MAKE) $@ 

${SLdata}/CC/corpus/%:
	cd ${corpusDir} && $(MAKE) $@ 

${SLdata}/CL/corpus/%:
	cd ${corpusDir} && $(MAKE) $@ 

CV/corpus/%: ${SLdata}/CV/corpus/%
	mkdir -p "CV/corpus"
	cp --recursive $< $@

PR/corpus/%: ${SLdata}/PR/corpus/%
	mkdir -p "PR/corpus"
	cp --recursive $< $@

XX/corpus/%: ${SLdata}/XX/corpus/%
	mkdir -p "XX/corpus"
	cp --recursive $< $@

CC/corpus/%: ${SLdata}/CC/corpus/%
	mkdir -p "CC/corpus"
	cp --recursive $< $@

CL/corpus/%: ${SLdata}/CL/corpus/%
	mkdir -p "CL/corpus"
	cp --recursive $< $@


SL-clean:
	rm -rf C*/corpus C*/predict C*/trained C*/output.sql

${jsreJar}:
	cd "${jsreBase}" && ant clean jar
