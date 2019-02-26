
#  Copyright (c) 2018, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>

Processors=2 # defaulf
expTyp_Upper=$(shell echo $(expTyp) | tr a-z A-Z)# convert to upper case
Kernel_Upper=$(shell echo $(Kernel)| tr a-z A-Z)# convert to upper case


help:
	$(info use 'make experiment \
		Kernel="" \
		expTyp="" \
		InputFile="" \
		TrainFile="" \
		TestFile="" \
		Processors=""')
	@echo
	@echo "Where:"
	@echo "     Kernel      :   Type of Kernel(APG|SL)."
	@echo "     expTyp      :   Type of experiment (CV|PR|XX)."
	@echo "     InputFile   :   Input file (.xml). Use this parameter only in case of CV or PR."
	@echo "     TrainFile   :   Training file (.xml). Use this parameter only in case of XX."
	@echo "     TestFile    :   Test file (.xml). Use this parameter only in case of XX."

experiment: check_parm experiment_run

check_parm:
ifeq ($(expTyp_Upper),)
	$(error FATAL ERROR: Variable expTyp undefined.)
endif
ifeq ($(Kernel_Upper),)
	$(error FATAL ERROR: Variable Kernel undefined.)
endif
	
ifneq ($(expTyp_Upper),$(filter $(expTyp_Upper),CV PR XX))
	$(error invalid or missing expType:"$(expTyp_Upper)". Type of experiment expTyp is (CV|PR|XX))
endif
ifneq ($(Kernel_Upper),$(filter $(Kernel_Upper),APG SL))
	$(error invalid or missing Kernel:"$(Kernel_Upper)". Type of Kernel is (APG|SL))
endif

experiment_run:
	$(MAKE) kernel-$(Kernel_Upper)-$(expTyp_Upper)
	
kernel-APG-CV:
	bash APG_Pipeline.sh -t CV -f $(InputFile) -p $(Processors)

kernel-APG-PR:
	bash APG_Pipeline.sh -t PR -f $(InputFile) -p $(Processors)
	python SetInteractionPrediction.py -k $(Kernel_Upper) -t $(expTyp_Upper) -i $(InputFile) -r output.sql -o output.apg.xml

kernel-APG-XX:
	$(MAKE) kernel-APG-XX-train
	$(MAKE) kernel-APG-XX-test
	python SetInteractionPrediction.py -k $(Kernel_Upper) -t $(expTyp_Upper) -i $(TestFile) -r output.sql -o output.apg.xml

kernel-APG-XX-train:
	bash APG_Pipeline.sh -t XX -f $(TrainFile) -x train -p $(Processors)

kernel-APG-XX-test:
	bash APG_Pipeline.sh -t XX -f $(TestFile) -x test -p $(Processors)



kernel-SL-CV:
	bash SL_Pipeline.sh -t CV -f $(InputFile) -p $(Processors)

kernel-SL-PR:
	bash SL_Pipeline.sh -t PR -f $(InputFile) -p $(Processors)
	python SetInteractionPrediction.py -k $(Kernel_Upper) -t $(expTyp_Upper) -i $(InputFile) -r output.sql -o output.sl.xml

kernel-SL-XX:
	$(MAKE) kernel-SL-XX-train
	$(MAKE) clean-SL
	$(MAKE) kernel-SL-XX-test
	python SetInteractionPrediction.py -k $(Kernel_Upper) -t $(expTyp_Upper) -i $(TestFile) -r output.sql -o output.sl.xml

kernel-SL-XX-train:
	bash SL_Pipeline.sh -t XX -f $(TrainFile) -x train -p $(Processors)

kernel-SL-XX-test:
	bash SL_Pipeline.sh -t XX -f $(TestFile) -x test -p $(Processors)


clean-all: clean-APG clean-SL

clean-APG: clean-APG-pre-steps clean-APG-kernel-steps

clean-APG-pre-steps:
	@cd CPI-corpora-preparing && \
		rm -rf bllip-parser/DS/ bllip-parser/DS*.txt && \
		rm -rf export_step1/DS* && \
		rm -rf export_step3/DS* export_step3/charniak-johnson/DS* && \
		rm -rf export_step4/DS/ export_step4/DS* && \
		rm -rf export_step6/CV/ export_step6/splits-test-train/ export_step6/DS* && \
		rm -rf step5_copied_from_3/DS* step5_copied_from_3/test* && \
		rm -rf splitting/DS/ splitting/DS* && \
		cd ..

clean-APG-kernel-steps:
	@cd ppi-benchmark && \
		rm -rf Corpora/APG/ && \
		rm -rf Experiments/APG/*/ && \
		cd ..

clean-SL: clean-SL-pre-steps clean-SL-kernel-steps

clean-SL-pre-steps:
	@cd ppi-benchmark/ && \
		rm -rf Parsing/DS/ && \
		rm -rf Corpora/Work/ Corpora/SL/ Corpora/Splits/*/ Corpora/Original/ Corpora/Original-Modified/ Corpora/splits-test-train/ && \
		rm -rf Corpora/Syntax-Tree-Learning-Format/DS* && \
		cd ..

clean-SL-kernel-steps:
	@cd ppi-benchmark && \
		rm -rf Experiments/SL/CV/ Experiments/SL/PR/ Experiments/SL/XX/ && \
		cd ..
