# a script for running all experiments

include ../Makefile.config

SYNKERNELS=ST SST PT
REGULARKERNELS=SpT kBSPS
SIMPLEKERNELS=SL cosine edit APG
#KimKernelTypeTest=lex

STOREDIR=$(if $(filter $(KERNEL),$(SYNKERNELS)),/ST-SST-PT/$(KERNEL)/$(expType)/$(CORPUS),$(if $(filter $(KERNEL),Kim),/KimKernel/$(expType)/*/$(CORPUS),$(if $(filter $(KERNEL),$(SIMPLEKERNELS)),/$(KERNEL)/$(expType),$(if $(filter $(KERNEL),$(REGULARKERNELS)),/$(KERNEL)/$(expType)/$(CORPUS),))))

help:
	$(info use 'make experiment \
		Corpora="$(CORPORA)" \
		Kernel="$(foreach k,$(KERNELS),$(if $(filter Kim,$k),$k,$k |))" \
		expType="$(foreach e,$(EXPTYPES),$(if $(filter CL,$e),$e,$e |))"')


# usage: make experiment Corpora="AIMed BioInfer HPRD50 IEPA LLL" Kernel="one of ${Kernels}" expType="CV" | "CC" | "CL"

experiment:
	$(MAKE) kernel-$(Kernel) 

experiment-test: 
	$(MAKE) kernel-$(Kernel) test=1

kernel-ST:
	$(MAKE) kernel-core kernelHome="$(runSynTree)" Kernel=ST

kernel-SST:
	$(MAKE) kernel-core kernelHome="$(runSynTree)" Kernel=SST

kernel-PT:
	$(MAKE) kernel-core kernelHome="$(runSynTree)" Kernel=PT

kernel-SpT:
	$(MAKE) kernel-core kernelHome="$(runSpT)" Kernel=SpT

kernel-kBSPS:
	$(MAKE) kernel-core kernelHome="$(runkBSPS)" Kernel=kBSPS

kernel-APG: update-apgconfig
	$(MAKE) kernel-core Kernel=APG

kernel-SL:
	cd SL && $(MAKE) jsre-core expType=$(expType) CORPORA="$(Corpora)"

kernel-cosine:
	$(error Not implemented)

kernel-edit:
	$(error Not implemented)

kernel-Kim:
	$(MAKE) kernel-core Kernel=Kim

kernel-core:
	$(MAKE) check-corpus CORPUS="$(Corpora)"
	$(MAKE) check-kernel KERNEL="$(Kernel)"
	$(MAKE) check-expType EXPTYPE="$(expType)"
ifeq ($(Kernel),Kim)
	cd $(expDir)/KimKernel && bash -c "corpusDir='$(corpusDir)' MEM='$(MEM3)' FayruzovAllDirs='${FayruzovAllDirs}' KimKernel='1' FayruzovCP='$(FayruzovCP)' propsDir='${propsDir}' test='$(test)' allCorpora='$(Corpora)' kernels='$(KimKernelType)' expType='$(expType)' ./execute-KimKernel.sh"
  endif
  ifneq ($(filter $(Kernel),$(REGULARKERNELS)),) # kBSPS, SpT
	$(MAKE) $(learner)
	cd $(expDir)/$(Kernel) && bash -c "corpusDir='$(corpusDir)' learner=$(learner) tester=$(tester) test='$(test)' allCorpora='$(Corpora)' kernels='$(Kernel)' expType='$(expType)' ./execute-$(Kernel).sh"
  endif
  ifeq ($(Kernel),APG)
    ifeq ($(test),1) 
	cd $(expDir)/APG && $(MAKE) apg-$(expType) allCorpora="$(TEST_CORPORA)"
    else
	cd $(expDir)/APG && $(MAKE) apg-$(expType) allCorpora="$(Corpora)"
    endif
  endif	
ifneq ($(filter $(Kernel),$(SYNKERNELS)),) #ST, SST, PT
	$(MAKE) $(learner)
	cd $(expDir)/ST-SST-PT && bash -c "corpusDir='$(corpusDir)' learner=$(learner) tester=$(tester) test='$(test)' allCorpora='$(Corpora)' kernels='$(Kernel)' expType='$(expType)' ./execute-syntree.sh"
endif

update-apgconfig: ${expDir}/APG/apgconfig.py.orig
	cp ${expDir}/APG/apgconfig.py.orig ${expDir}/APG/apgconfig.py
	sed -i "s@path=''@path='$(expDir)/APG'@" ${expDir}/APG/apgconfig.py
	sed -i "s@source=''@source='$(kernelDir)/airola/source'@" ${expDir}/APG/apgconfig.py


check-storedir:
	@test -d "$(STOREDIR)" || $(MAKE) err MSG="Incorrect storage directory, check the value of STOREDIR"

# usage: make output2db Corpora="AIMed BioInfer HPRD50 IEPA LLL" Kernel="one of ${Kernels}" expType="CV CC CL"

output2db:
	$(MAKE) output2db-splitter Kernel="$(Kernel)" expType="$(expType)" Corpora="$(Corpora)"

output2db-splitter:
	$(MAKE) check-expType-more EXPTYPE="$(expType)"
	$(MAKE) check-kernel KERNEL="$(Kernel)"
ifeq ($(filter $(Kernel),$(SIMPLEKERNELS)),$(Kernel))
	echo -n $(foreach e,${expType},\
		$(shell echo -n $(MAKE) output2db-simple-core KERNEL=$(Kernel) expType="$e" '@'))  \
	| $(XARGSquiet) -d '@' --max-args 1 bash -c
else
	$(MAKE) check-corpus CORPUS="$(Corpora)"
	echo -n $(foreach c,${Corpora},$(foreach e,${expType},\
		$(shell echo -n $(MAKE) output2db-core KERNEL=$(Kernel) expType="$e" CORPUS=$(c) '@')))  \
	| $(XARGSquiet) -d '@' --max-args 1 bash -c
endif

output2db-core:
#	find ${expDir} -path '*${STOREDIR}/*' -name '*.sqllog' | $(XARGS) -r rm
	find ${expDir} -path "*${STOREDIR}/out-CV-*-1to2-k1-3-LED-00-1166/*-*-*-*" -name '*.sql' \
	| $(XARGS) -I'{}' bash -c "${PSQL} -f {} --single-transaction 2>&1 | tee {}.sqllog"

output2db-simple-core:
	find ${expDir}/$(STOREDIR) -name '*.sql' -exec bash -c "${PSQL} -f {} --single-transaction 2>&1 | tee {}.sqllog" \;


check-inputs:
	$(MAKE) check-expType EXPTYPE=$(EXPTYPE)
	$(MAKE) check-corpus CORPUS=$(CORPUS)

.PHONY: help check-inputs output2db-simple-core
