
# Creation of learning format for shallow linguistic kernels

SL_TOKENIZER=Charniak-Lease
#SL_PARSER=Charniak-Johnson-McClosky

SL_CV_LF=$(foreach c,$(CORPORA),${SLdata}/CV/corpus/${c})

.PRECIOUS: ${SLdata}/CV/corpus/%
${SLdata}/CV/corpus/%: ${stlfDir}/%.xml
	$(MAKE) "${LF_JAR}"
	mkdir -p "${SLdata}/CV/corpus"
	$(JAVA) ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
		org.learningformat.api.JSRE_Tranformer \
			-s "${splitDir}" \
			-o "${SLdata}/CV/corpus" \
			-t '${SL_TOKENIZER}' \
			--porter \
			-i "$<" \
			> "$@.log" 2>&1

#			--skip-train \

.PRECIOUS: ${SLdata}/CC/corpus/%
${SLdata}/CC/corpus/%: ${SL_CV_LF}
	for cc in $(CORPORA) ; do \
		dir="${SLdata}/CC/corpus/$$cc" ; \
		echo "Copying corpus '$$cc' for CC experiment into '$$dir' ..." ; \
		mkdir -p "$$dir" ; \
		find "${SLdata}/CV/corpus/$$cc/" -name "test*.txt" -exec cat "{}" \; > "$$dir/corpus.txt" ; \
	done


.PRECIOUS: ${SLdata}/CL/corpus/%
${SLdata}/CL/corpus/%: ${SL_CV_LF}
	for cc in $(CORPORA) ; do \
		dir="${SLdata}/CL/corpus/$$cc" ; \
		echo "Copying corpus '$$cc' for CL experiment into '$$dir' ..." ; \
		mkdir -p "$$dir" ; \
		find "${SLdata}/CV/corpus/$$cc/" -name "test*.txt" -exec cat "{}" \; > "$$dir/corpus.txt" ; \
	done

CV_LF: ${SL_CV_LF}


# dummy:
# 	for c1 in $(CORPORA) ; do \
# 		dir="CC/corpus/$$c1" ; \
# 		echo "Creating CL learning format for corpus '$$c1' into '$$dir' ..." ; \
# 		rm -rf "$$dir" ; \
# 		mkdir -p "$$dir" ; \
# 		find "$</$$c1/" -name "test*.txt" -exec cat "{}" \; > "$$dir/test.txt" ; \
# 		for c2 in $(CORPORA) ; do \
# 			if [ "X$$c1" != "X$$c2" ] ; \
# 			then \
# 				find "$</$$c2/" -name "test*.txt" -exec cat "{}" \; >> "$$dir/train.txt" ; \
# 			fi \
# 		done \
# 	done

# SL-CC: ${LF_JAR}
# 	mkdir -p "${SLdata}/CC/corpus"
# 	echo -n $(CorporaXML) | \
# 	$(XARGSd) -I'{}' java ${MEM1} -cp "${LF_JAR}${SEP}${LF_CLASSPATH}" \
# 		org.learningformat.api.JSRE_Tranformer \
# 			-e "CC" \
# 			-o "${SLdata}/CC/corpus" \
# 			-t '${SL_TOKENIZER}' \
# 			--porter \
# 			-i '{}'



#-l "${slData}/CV/tmp/tst.txt.txp" \

