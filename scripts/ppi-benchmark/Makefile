include Makefile.config

all: 

init-schema: 
	cd ${dbDir} && $(MAKE)

# archive outputs of intermediate processing steps
zip:
	zip -r ppi-benchmark1 `basename ${corpusDir}`/`basename ${origDir}`/*.xml \
		`basename ${corpusDir}`/`basename ${stlfDir}`/*.xml \
		`basename ${expDir}`/kBSPS/CV/LLL/out-CV-LLL-2to2-k0-2-LED-00-1166/* \
		`basename ${expDir}`/kBSPS/CL/BioInfer/out-CL-BioInfer-1to3-k0-2-LED-000333/* \
		`basename ${expDir}`/kBSPS/CC/LLL/out-CC-LLL-1to2-k0-1-LED-000133/* 
	zip -r ppi-benchmark2 `basename ${corpusDir}`/`basename ${lfDir}`/*


test-dependencies:
	svn --version
	psql --version
	java -version
	javac -version
	ant -version
	gcc --version
	flex --version
	python --version
	python -c "import numpy; print numpy.version.version"
	$(info All dependencies met.)


# zip1
# Original corpora
# classifier input
# CV samples
# CL samples
# CC samples

# zip2
# Syntax-tree learning format
