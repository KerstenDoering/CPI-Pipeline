Processors=2 # defaulf

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
	@echo "     Kernel      :   Type of Kernel(APG|SL)"
	@echo "     expTyp      :   Type of experiment (CV|PR|XX)"
	@echo "     InputFile   :   Input file (.xml). Use this parameter only in case of CV or PR"
	@echo "     TrainFile   :   Training file (.xml). Use this parameter only in case of XX"
	@echo "     TestFile    :   Test file (.xml). Use this parameter only in case of XX"


experiment:
	$(MAKE) kernel-$(Kernel)-$(expTyp) 


kernel-APG-CV:
	bash APG_pipeline.sh -t CV -f $(InputFile) -p $(Processors)

kernel-APG-PR:
	bash APG_pipeline.sh -t PR -f $(InputFile) -p $(Processors)

kernel-APG-XX:
	$(MAKE) kernel-APG-XX-train
	$(MAKE) kernel-APG-XX-test

kernel-APG-XX-train:
	bash APG_pipeline.sh -t XX -f $(TrainFile) -x train -p $(Processors)

kernel-APG-XX-test:
	bash APG_pipeline.sh -t XX -f $(TestFile) -x test -p $(Processors)

clean:
	
