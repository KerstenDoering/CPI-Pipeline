
# Creation of learning format for syntax tree based kernels

include ../Makefile.config
include Makefile.SL

TMPDIR=/tmp/

# Parsing

PARSEBASEDIR=${baseDir}/Parsing
RERANKINGPARSER=${PARSEBASEDIR}/Charniak-Lease-2006Aug-reranking-parser
BIOPARSINGMODEL=${PARSEBASEDIR}/Models/McClosky-2009
GENIATAGGER_DIR=${PARSEBASEDIR}/geniatagger

RERANKINGPARSER_URL=ftp://ftp.cs.brown.edu/pub/nlparser/reranking-parserAug06.tar.gz
BIOPARSINGMODEL_URL=http://bllip.cs.brown.edu/download/bioparsingmodel-rel1.tar.gz
GENIATAGGER_URL=http://www.nactem.ac.uk/tsujii/GENIA/tagger/geniatagger-3.0.1.tar.gz

# The patch needed to compile the Charniak Lease parser
RERANKINGPARSER_PATCH=${PARSEBASEDIR}/Charniak-Lease-2006Aug-reranking-parser.patch
GENIATAGGER_PATCH=${PARSEBASEDIR}/geniatagger-3.0.1.patch

# The directory to which the files are extracted
RERANKINGPARSER_BASE=${RERANKINGPARSER}/reranking-parser
BIOPARSINGMODEL_BASE=${BIOPARSINGMODEL}/biomodel
GENIATAGGER_BASE=${GENIATAGGER_DIR}/geniatagger-3.0.1


parseIt=${RERANKINGPARSER_BASE}/first-stage/PARSE/parseIt
bestparses=${RERANKINGPARSER_BASE}/second-stage/programs/features/best-parses
parser=${BIOPARSINGMODEL_BASE}/parser
featuresgz=${BIOPARSINGMODEL_BASE}/reranker/features.gz
weightsgz=${BIOPARSINGMODEL_BASE}/reranker/weights.gz
geniatagger=${GENIATAGGER_BASE}/geniatagger



CVDir=${lfDir}/CV
CLDir=${lfDir}/CL
CCDir=${lfDir}/CC

include Makefile.Fayruzov

idCCKernels=CUSTOM_KERNEL MOSCHITTI

XARGSd=$(XARGS) -d ' '

all: pre-steps main-steps post-steps

all-kBSPS: pre-steps main-steps-kBSPS post-steps-kBSPS

pre-steps: download-benchmark repair-BioInfer compile

main-steps: clean main-steps-syntree main-steps-kBSPS

post-steps: clean post-steps-kBSPS idVersion

post-steps-kBSPS: createCC createCL 

generate-enriched-xml: ${EnrichedXML}

create-SL-LF: check-ST-dirs $(foreach c,$(CORPORA),$(foreach e,${EXPTYPES},${SLdata}/${e}/corpus/${c}))
create-ST-LF: check-ST-dirs $(foreach c,$(CORPORA),${stlfDir}/${c}.xml)

check-ST-dirs:
	@echo Make sure '$$origDir' and '$$stlfDir' are not the same.
	@test "`readlink -f ${origDir}`" != "`readlink -f ${stlfDir}`"

echo-corpora:
	@echo 'Current corpora:'
	@echo "CORPORA='$(CORPORA)'"

#{EnrichedXML}: ${CorporaXML} SynTree-step1 SynTree-step2 SynTree-step3 SynTree-step4 SynTree-step5

download-benchmark: ${BenchmarkXML}

main-steps-syntree: generate-enriched-xml SynTree-step6

main-steps-kBSPS: kBSPS-step6

${BenchmarkXML}:
	#@echo test  1 = 1 $(foreach c,$(BENCHMARKCORPORA),-a -f "$(origDir)/$(c).xml") 
	#@echo test  1 = 1 $(foreach c,$(BENCHMARKCORPORA),-a -f "$(origDir)/$(c).xml")  || echo missing 
ifeq ($(shell test  1 = 1 $(foreach c,$(BENCHMARKCORPORA),-a -f "$(origDir)/$(c).xml")  || echo missing ), missing)
	wget -nc http://mars.cs.utu.fi/PPICorpora/AImed-learning-format.xml.gz 
	wget -nc http://mars.cs.utu.fi/PPICorpora/BioInfer-learning-format.xml.gz
	wget -nc http://mars.cs.utu.fi/PPICorpora/HPRD50-learning-format.xml.gz
	wget -nc http://mars.cs.utu.fi/PPICorpora/IEPA-learning-format.xml.gz
	wget -nc http://mars.cs.utu.fi/PPICorpora/LLL-learning-format.xml.gz
	rm -rf ${origDir}
	mkdir -p ${origDir}
	mv *.gz ${origDir}
	gunzip -f ${origDir}/*.gz
	find ${origDir} -name '*.xml' | sed 's/-learning-format.xml//' | xargs -I'{}' mv '{}-learning-format.xml' '{}.xml'
	mv ${origDir}/AImed.xml ${origDir}/AIMed.xml
endif

repair-BioInfer: ${origDir}/BioInfer.xml.repaired


${origDir}/BioInfer.xml.repaired: ${origDir}/BioInfer.xml
	cp "$<" "$<.ori"
	./repair-BioInfer.pl < "$<.ori" > "$<.repaired"
	cp "$<.repaired" "$<"


compile: ${LF_JAR}


list-CorporaXML:
	echo "$(CorporaXML)"

# Step 1
# Extracts sentences from the original XML 
# Result is written in $file-ptb-s.txt

.PRECIOUS: ${workDir}/%.xml-ptb-s.txt
${workDir}/%.xml-ptb-s.txt: ${origDir}/%.xml
	$(MAKE) "${LF_JAR}" # do not add to dependencies
	mkdir -p "${workDir}"
	( \
	${JAVA} ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
		org.learningformat.transform.PtbRawSentenceTransformer \
		-f "$<" -o "$@.tmp" \
		> "$@.log" 2>&1 \
	&& mv "$@.tmp" "$@" \
	) || ( cat "$@.log" ; exit 1 )

#SynTree-step1: ${LF_JAR}
#	echo -n $(CorporaXML) | \
#	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.PtbRawSentenceTransformer -f '{}'
	
# Step 2 - Parsing
# Results in two files -parsed.txt and -parsed.err
# ${parseIt} ${bestparses} ${parser} ${featuresgz} ${weightsgz}
.PRECIOUS: ${workDir}/%-ptb-s.txt-parsed.txt
${workDir}/%-ptb-s.txt-parsed.txt: ${workDir}/%-ptb-s.txt ${parseIt} ${bestparses} ${parser} ${featuresgz} ${weightsgz}
	"${parseIt}" -t4 -l399 -N50 "${parser}/" "$<" 2>"$@.parseIt.err" \
	| ${bestparses} -ls "${featuresgz}" "${weightsgz}" \
		> "$@.tmp" 2>"$@.bestparses.err" \
	&& mv "$@.tmp" "$@"

# SynTree-step2: ${parseIt} ${bestparses} ${parser} ${featuresgz} ${weightsgz}
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' \
# 		$(MAKE) '{}-ptb-s.txt-parsed.txt'

# Step 3 - Injects parse result into XML
# requires original .xml file and the .ptb-s.txt-parsed.txt file
.PRECIOUS: ${workDir}/%.inj1
${workDir}/%.inj1: ${workDir}/%-ptb-s.txt-parsed.txt ${LF_JAR}
	( \
	${JAVA} ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
		org.learningformat.transform.PtbTreeInjector \
		-f "${origDir}/$*" -p "$<" -o "$@.tmp" -i \
	> "$@.log" 2>&1 \
	&& mv "$@.tmp" "$@" \
	) || ( cat "$@.log" ; exit 1 )

# SynTree-step3: ${LF_JAR}
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.PtbTreeInjector -f '{}' -p '{}'-ptb-s.txt-parsed.txt -o '{}'.inj1 -i

# Step 4 - Mapping between POS and text
# requires .inj1 file and creates .inj1-bracketing-tokens.txt
.PRECIOUS: ${workDir}/%.inj1-bracketing-tokens.txt
${workDir}/%.inj1-bracketing-tokens.txt: ${workDir}/%.inj1 
	$(MAKE) ${LF_JAR}
	( \
	${JAVA} ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
		org.learningformat.transform.BracketingTokenMapper \
		< "$<" > "$@.tmp" \
		2> "$@.log" \
	&& mv "$@.tmp" "$@" \
	) || ( cat "$@.log" ; exit 1 )

# SynTree-step4: ${LF_JAR}
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.BracketingTokenMapper '{}.inj1'

# Step 5 - Injects the bracketing into the xml file
.PRECIOUS: ${workDir}/%.inj1.inj2
${workDir}/%.inj1.inj2: ${workDir}/%.inj1-bracketing-tokens.txt
	$(MAKE) "${LF_JAR}"
	( \
	${JAVA} ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
		org.learningformat.transform.PtbTreeInjector \
		-f "${workDir}/$*.inj1" -t "$<" -o "$@.tmp" \
	> "$@.log" 2>&1 \
	&& mv "$@.tmp" "$@" \
	) || ( cat "$@.log" ; exit 1 )

.PRECIOUS: ${stlfDir}/%.xml
${stlfDir}/%.xml: ${workDir}/%.xml.inj1.inj2
	mkdir -p "${stlfDir}"
	cp "$<" "$@"

# SynTree-step5: ${LF_JAR}
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.PtbTreeInjector -f '{}.inj1' -t '{}.inj1-bracketing-tokens.txt' -o '{}.inj1.inj2'
# 	rm -rf ${stlfDir}
# 	mkdir -p ${stlfDir}
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' bash -c 'cp "{}.inj1.inj2" ${stlfDir}/`basename "{}"`'

# Step 6 - Creates the splits

SynTree-step6: ${LF_JAR}
	@for c in "$(CORPORA)" ; \
	do \
		if test -d "${splitDir}/$$c" ; then echo "" ; else $(MAKE) err MSG="Missing split directory: ${splitDir}/$$c" ; fi \
	done 
	rm -rf ${CVDir}/MOSCHITTI
	mkdir -p ${CVDir}/MOSCHITTI
	echo -n $(foreach c,$(CorporaXML),${stlfDir}/$(shell basename $(c))) | \
	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.SvmLightTreeKernelTransformer -f '{}' -m -s ${splitDir} -o ${CVDir}
	rm -rf ${CVDir}/CUSTOM_KERNEL
	mkdir -p ${CVDir}/CUSTOM_KERNEL
	echo -n $(foreach c,$(CorporaXML),${stlfDir}/$(shell basename $(c))) | \
	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.SvmLightTreeKernelTransformer -f '{}' -c -s ${splitDir} -o ${CVDir}

clean:
	rm -rf "${workDir}" "${origDir}/BioInfer.xml.ori"  "${origDir}/BioInfer.xml.repaired"

kBSPS-step6: ${LF_JAR}
	rm -rf "${CVDir}/CUSTOM_KERNEL-b*"
	@test -d "$(CVDir)" || mkdir -p "${CVDir}"
	@echo -n $(CorporaXML) | \
	$(XARGSd) -t -I'{}' \
	bash -c "$(JAVA) ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" org.learningformat.transform.SvmLightDependencyTreeKernelTransformer -f '{}' --qmin 1 --qminmax 2 --qmaxmin 2 --qmax 3 -k 1 -s ${splitDir} -o ${CVDir}";

createCC:
	rm -rf ${CCDir}
	@$(MAKE) createCCcore EXTENSION=txt FINDPARAMS='-mindepth 2 -type d'

createCCcore:
ifndef EXTENSION
	@echo "parameter (EXTENSION) is undefined" > /dev/stderr && exit 1
else
  ifeq ($(EXTENSION), txt)
	find ${CVDir} -mindepth 1 -maxdepth 1 -type d \
	| $(XARGS) --max-procs 1 --max-args 1 basename \
	| $(XARGS) -I'{}' mkdir -p ${CCDir}/'{}'
  else
    ifneq ($(EXTENSION), txt.id)
		echo "unknown extension: $(EXTENSION), accepted are 'txt' and 'txt.id'" > /dev/stderr && exit 1
    endif
  endif
	find ${CVDir} ${FINDPARAMS} \
	| sed 's/-folds//' \
	| $(XARGS) -I'{}' -t bash -c 'cat {}-folds/*.${EXTENSION} > ${CCDir}/`basename \`dirname {}\``/`basename {}`.${EXTENSION}'
endif

createCL:
	@$(MAKE) createCLcore EXTENSION=txt \
		WHICHKERNELS="$(foreach f,$(shell find ${CCDir} -mindepth 1 -maxdepth 1 -type d),$(shell basename $f))"

createCLcore:
	$(foreach c,${CORPORA},$(foreach k,$(WHICHKERNELS),sh -c "$(MAKE) createCLcorpus CORPUS='$c' KERNELTYPE='$k' EXTENSION='$(EXTENSION)' " ; ))

createCLcorpus:
ifndef KERNELTYPE
	@$(MAKE) err MSG="parameter (KERNELTYPE) is undefined"
endif
ifndef CORPUS
	@$(MAKE) err MSG="parameter (CORPUS) is undefined"
endif
ifndef EXTENSION
	@$(MAKE) err MSG="parameter (EXTENSION) is undefined"
else
  ifeq ($(EXTENSION),txt)
	rm -rf ${CLDir}/${KERNELTYPE}/${CORPUS}-folds
	mkdir -p ${CLDir}/${KERNELTYPE}/${CORPUS}-folds
  else
    ifeq ($(EXTENSION),txt.id)
      ifneq ($(shell find "${CCDir}/${KERNELTYPE}" -maxdepth 1 -name "*.${EXTENSION}" | wc -l),$(NUMCORPORA))
		@$(MAKE) err MSG="*.txt.id files (5) are missing"
      endif
	  rm -rf "${CLDir}/${KERNELTYPE}/${CORPUS}-folds/*.${EXTENSION}"
    else
	  echo "unknown extension: '$(EXTENSION)', accepted are 'txt' and 'txt.id'" > /dev/stderr && exit 1
    endif
  endif
	cp "${CCDir}/${KERNELTYPE}/${CORPUS}.${EXTENSION}" "${CLDir}/${KERNELTYPE}/${CORPUS}-folds/1.${EXTENSION}"
	find ${CCDir}/${KERNELTYPE} -name '*.${EXTENSION}' -not -name '${CORPUS}.${EXTENSION}' \
	| $(XARGS) --max-procs 1 -I'{}' -t bash -c 'cat "{}" >> ${CLDir}/${KERNELTYPE}/${CORPUS}-folds/0.${EXTENSION}'
endif

update:
	svn up ${LFbaseDir}

idVersion: idCV idCC idCL

idCV: 
	echo $(foreach c,${CORPORA},$(shell make idCVcore CORPUS=$c > /dev/stderr))

idCVcore: $(shell find ${CVDir} -mindepth 1 -maxdepth 1 -type d -name "CUSTOM_KERNEL-b*" 2> /dev/null | head -1 )
	@find ${CVDir} -mindepth 1 -maxdepth 1 -type d \( -name "CUSTOM_KERNEL" -or -name "MOSCHITTI" \) \
	| $(XARGS) --max-procs 1 -I'{}' bash -c "DIR1='$<' DIR2='{}' CORPUS=${CORPUS} ./extractCV.sh" 

idCC: 
	make createCCcore EXTENSION=txt.id FINDPARAMS="-mindepth 1 -type d \( -path '*CUSTOM_KERNEL/*' -or -path '*MOSCHITTI/*' \)"

idCL:
	make createCLcore EXTENSION=txt.id WHICHKERNELS="$(idCCKernels)"


# add-ons

geniatagger: ${geniatagger}

${geniatagger}: download-geniatagger compile-geniatagger

download-geniatagger:
	@$(MAKE) download-extract DIRECTORY="$(GENIATAGGER_DIR)" URL="$(GENIATAGGER_URL)"

compile-geniatagger:
	@test -f "$(geniatagger)" || \
	( cd "$(GENIATAGGER_BASE)" \
		&& patch -p1 --forward --force --input "$(GENIATAGGER_PATCH)" \
		&& $(MAKE) clean \
		&& $(MAKE) \
	)

SCHEMA_EA=${dbDir}/init-errorAnalysis.sql
init-error-analysis-db: ${corpusDir}/tokenization2postgres.pl ${SCHEMA_EA} ${geniatagger}
	${PSQL} -f ${SCHEMA_EA}
	echo -n $(CorporaXML) \
	| $(XARGS) --max-procs 1  \
		"$<" '${geniatagger}' 'Charniak-Lease' \
	| tee "tokenization.sql" \
	| ${PSQL}

# parsing

parseIt: ${parseIt}

${bestparses} ${parseIt}: download-RerankingParser compile-RerankingParser
	@test -f "$@" || $(MAKE) err MSG="Reranking parser seems to be available, but $@ is missing"

download-RerankingParser:
	@$(MAKE) download-extract DIRECTORY="$(RERANKINGPARSER)" URL="$(RERANKINGPARSER_URL)"

compile-RerankingParser:
	@test -f "$(parseIt)" || \
	( cd "$(RERANKINGPARSER_BASE)" \
		&& patch -p1 --forward --force --input "$(RERANKINGPARSER_PATCH)" \
		&& $(MAKE) clean \
		&& $(MAKE) PARSE reranker-runtime )

${weightsgz} ${featuresgz}: download-McCloskyModel09
	@test -f "$@" ||	$(MAKE) err MSG="BioModel seems to be available, but $@ is missing"

${parser}: download-McCloskyModel09
	@test -d "$@" ||	$(MAKE) err MSG="BioModel seems to be available, but $@ is missing"

download-McCloskyModel09:
	@$(MAKE) download-extract DIRECTORY="$(BIOPARSINGMODEL)" URL="$(BIOPARSINGMODEL_URL)"

dummy:
	@echo '<s ID123> Double quote: " Single quote: '"'"' Joined double quote" Two single quotes '"''"' Two joined single quotes'"''"'</s>' | "${parseIt}" -l399 -N50 "${parser}/" | ${bestparses} -s -l "${featuresgz}" "${weightsgz}"

.PHONY: update
