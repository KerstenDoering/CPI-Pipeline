#!/bin/bash

# example usage:
# time bash -c "find . -maxdepth 1 -mindepth 1 -type d | grep '[0-9]' | nice nice xargs -P8 -t --max-args 1 ./standoff2xml.sh > /dev/null"

## arguments 

if [ $# -eq 0 ]; then
  echo 1>&2 Usage: $0 '<input_directory>' ... 
  exit 127 
fi

DIR=$1
PREFIX=`basename ${DIR}`

## parameters
LF=/vol/home-vol3/wbi/solt/ppi-benchmark/Converters/learning-format-api/
#LF=/vol/home-vol3/wbi/thomas/workspace/ppi-benchmark/Converters/learning-format-api

CLASSPATH="${LF}/dist/lfapi.jar:${LF}/lib/*"
ENTRY="org.learningformat.standoff.Driver"

JAVA="/usr/bin/time --verbose java -XX:+UseCompressedOops"

OUTDIR=xml
LOGDIR=log

CORPUS=PMC

#PAIRS=intact.geneId.no-self.csv
PAIRS=/local/colonet/colonet/colonet/export/ppi/intact.geneId.no-self.csv


## main

mkdir -p "${OUTDIR}" "${LOGDIR}"
${JAVA} -cp "${CLASSPATH}" "${ENTRY}" \
		--out-file "${OUTDIR}/${PREFIX}.xml" \
		--pairs-file "${PAIRS}" \
		--with-pairs \
		--corpus "${CORPUS}"  \
	"${DIR}" \
	2>&1 | tee "${LOGDIR}/${PREFIX}.log"
