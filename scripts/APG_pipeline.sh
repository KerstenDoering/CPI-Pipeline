#! /bin/bash

#    Copyright (c) 2015, Kersten Doering, Ammar Qaseem, Elham Abbasian

#    This script executes the steps from the protein-protein-interaction pipeline of Tikk et al. (scripts/ppi-benchmark/Documentation/kernels-howto.pdf, (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).

VERSION=0.1

usage="$(basename "$0") [-h] [-f] [-x] [-p n] -- This script identifies functional compound-protein relationships.

where:
    -h  help.
    -f  Input file (default: DS.xml).
    -t  Type of experiment (CV, PR, XX).
    -x  Type of process(train or test). This parameter just used with XX.
    -p  Number of processors (default: 2)."


filename="DS.xml"
PROCESSES="2"

while getopts ":f:t:p:x:hv" option;
do
 case "${option}" in
 v) echo "CPI -Version $VERSION"
       exit 0;
       ;;
 h) echo "$usage"
       exit
       ;;
 f) filename=${OPTARG};; 
 t) ExpTyp=${OPTARG};;
 x) ProcessTyp=${OPTARG};;
 p) if [[ $OPTARG =~ ^[0-9]+$ ]];then
       PROCESSES=${OPTARG}
    else
       printf "illegal value for -%s\n" "$option"
       echo "$usage"
       exit
 
   fi
   ;;
 :) printf "missing argument for -%s\n" "$OPTARG"
       echo "$usage"
       exit 1
       ;;
 \?) printf "illegal option: -%s\n" "$OPTARG"
       echo "$usage"
       exit 1
       ;;
 esac
done

if [ ! -f generate_XML_files/DS/$filename ]; then
        echo "$filename" " -File not found!"
        exit 1
fi

if [ $filename != "DS.xml" ]
then

  cp -f generate_XML_files/DS/$filename generate_XML_files/DS/DS.xml

fi



echo "filename : " $filename
echo "PROCESSES : " $PROCESSES



# copy input files with the general XML format to the folder export_step1
cp generate_XML_files/DS/DS.xml CPI-corpora-preparing/export_step1/
cd CPI-corpora-preparing/export_step1/

# Step 1: extract all sentences from the XML file and enclose them in <s id>...</s> tags
# kernels-howto.pdf - Appendix C, Palaga’s Learning format API Java library
# Output: DS.xml-ptb-s.txt
echo "step 1 : Extract all sentences from the XML file ..."

java -jar preparing_parsing_input.jar -f DS.xml 


# Step 2: build a syntactic tree parse with part-of-speech tags using the BLLIP reranking parser (also known as Charniak-Johnson parser, Charniak parser, Brown reranking parser) - https://github.com/BLLIP/bllip-parser
# Output: DS.xml-ptb-s.txt-parsed.txt and -parsed.err
echo "step 2 : Build a syntactic tree ..."
cd ..
cp export_step1/DS.xml-ptb-s.txt bllip-parser/
cd bllip-parser/
rm -rf DS
mkdir DS/

python bllip_parser.py -i DS.xml-ptb-s.txt -c DS -p $PROCESSES

    
# add the identifiers from the input file in each line of the current output file
# Output: DS.xml-ptb-s.txt-parsed_modified.txt
# ToDo: include biomedical parsing model - debug (kernels-howto.pdf)
python merge_identifiers.py -c DS
cd ..
rm -rf export_step3/charniak-johnson/
mkdir -p export_step3/charniak-johnson/
cp bllip-parser/DS.xml-ptb-s.txt-parsed_modified.txt export_step3/charniak-johnson/


# Step 3: merge BLLIP parser results with the XML file from step 1 in  <bracketings>...</bracketings> tags for each sentence
# the dependency parses and the tokenization with character offsets and part-of-speech tags will also be generated within this step
# Output: file DS.xml.inj1
echo "step 3 : Merge BLLIP parser results with the XML file ..."
cp export_step1/DS.xml export_step3/
cd export_step3/
java -jar step_3_and_5_injection_lib.jar -f DS.xml -p DS.xml-ptb-s.txt-parsed_modified.txt -o DS.xml.inj1 -i


# Step 4: alignment of the character offsets in the original sentence with the parsed results (<bracketings>...</bracketings>)
# Output: DS.xml.inj1-bracketing-tokens.txt.
echo "step 4 : Alignment character offsets  ..."
cd ..

    
cp export_step3/DS.xml.inj1 export_step4/
cd export_step4/


##cd CPI-corpora-preparing/export_step4/  


# ---- This part added to solve the problem of insufficient memory(##)
rm -rf DS
rm -f DS.xml.inj1-bracketing-tokens.txt
mkdir DS/
# splitting DS.xml.inj1 into small chunk, each one contains one document
python xmlsplitter.py -c DS

#exit 1

# process each document individually, this process have to run sequentially to avoid the problem of insufficient memory 
for i in `seq 1  $( ls DS -1 | wc -l ) `; 
do
    let "j = $i -1 "
    java -jar step_4_BracketingTokenMapper.jar DS/$j.xml

    cat DS/$j.xml-bracketing-tokens.txt >> DS.xml.inj1-bracketing-tokens.txt
    
done        

#cd CPI-corpora-preparing
# Step 5: injection of the aligned character offsets to the XML file DS.xml.inj1 (<bracketings>...</bracketings>)e
# Output: DS.xml.inj1.inj2
echo "step 5 : Injection of the aligned character offsets to the XML file..."
cd ..
cp export_step4/DS.xml.inj1-bracketing-tokens.txt step5_copied_from_3/
# ToDo: combine directories 3 and 5, because they use the same JAR file
cp export_step3/DS.xml.inj1 step5_copied_from_3/
cd step5_copied_from_3
java -jar step_3_and_5_injection_lib.jar -f DS.xml.inj1 -t DS.xml.inj1-bracketing-tokens.txt -o DS.xml.inj1.inj2

if [ $ExpTyp = "XX" ] && [ $ProcessTyp = "train" ]
then
    
    gzip -c -f DS.xml.inj1.inj2 > train0.txt.gz
    echo "The training data set are pre-processed, output is \"CPI-corpora-preparing/step5_copied_from_3/train0.txt.gz\""
    #cd ../..
    exit
    
else
    gzip -c -f DS.xml.inj1.inj2 > test0.txt.gz
fi
       


if [ $ExpTyp = "CV" ]
then
    # Step 6: rename the file DS.xml.inj1.inj2 to DS.xml and (document-level) splitting of the sentences for 10-fold cross-validation (randomSplit.pl was slightly modified to generate the correct all-paths graph-specific format from the given input file - marked with "Kersten")
    # Output: DS/test-1 - DS/test-2
    
    echo "step 6 ..."
    cd ..
    rm -rf export_step6/CV/DS ##
    cp step5_copied_from_3/DS.xml.inj1.inj2 splitting
    cd splitting
    mv DS.xml.inj1.inj2 DS.xml
    rm -rf DS ##
    ./randomSplit.pl DS.xml 

    # the cross-validation files need to be renamed and the folders that need to be copied to the directory ppi-benchmark as input files for the make-experiment steps will be prepared
    # zip all cross-validation text files - test0.txt contains data to evaluate one of the ten parts and train0.txt contains the rest of the data for the training process
    # read old cross-validation parts (PubMed IDs) and merge them with new data set identifiers of DS

    python rename_files_splitting.py -c DS
        
    
    cd ..

    rm -rf export_step6/splits-test-train
    mkdir export_step6/splits-test-train

    rm -rf export_step6/splits-test-train/DS
    mkdir export_step6/splits-test-train/DS

    cp splitting/DS/* export_step6/splits-test-train/DS/
    cp splitting/DS.xml export_step6/

    cd export_step6
        


    rm -rf CV
    mkdir -p CV/
    mkdir -p CV/DS/

    python split_AllGraphTransformer_CV.py -c DS ##

    cd CV/DS
    
    gzip -f *.txt
    
    cd ../..    
    
    
fi



echo "copying files ..."
cd ../..



mkdir -p ppi-benchmark/Corpora/Original/
cp CPI-corpora-preparing/export_step1/DS.xml ppi-benchmark/Corpora/Original/
mkdir -p ppi-benchmark/Corpora/Original-Modified/


mkdir -p ppi-benchmark/Corpora/APG/
mkdir -p ppi-benchmark/Corpora/APG/$ExpTyp/
mkdir -p ppi-benchmark/Corpora/APG/$ExpTyp/corpus/
rm -rf ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS
mkdir -p ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS/


if [ $ExpTyp = "CV" ]
then

    mkdir -p ppi-benchmark/Corpora/splits-test-train/ #
    mkdir -p ppi-benchmark/Corpora/splits-test-train/DS/ #
    
    cp CPI-corpora-preparing/export_step6/splits-test-train/DS/* ppi-benchmark/Corpora/splits-test-train/DS/
    cp CPI-corpora-preparing/splitting/DS.xml ppi-benchmark/Corpora/Original-Modified/

    cp -r CPI-corpora-preparing/export_step6/$ExpTyp/DS/ ppi-benchmark/Corpora/APG/$ExpTyp/corpus/

elif [ $ExpTyp = "PR" ]
then

    mv -f CPI-corpora-preparing/step5_copied_from_3/test0.txt.gz ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS/test0.txt.gz
    cp -f training/train0.txt.gz ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS/train0.txt.gz

elif [ $ExpTyp = "XX" ]
then

    mv -f CPI-corpora-preparing/step5_copied_from_3/test0.txt.gz ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS/test0.txt.gz
    mv -f CPI-corpora-preparing/step5_copied_from_3/train0.txt.gz ppi-benchmark/Corpora/APG/$ExpTyp/corpus/DS/train0.txt.gz

fi



# start the experiment
echo "run APG pipeline ..."
mkdir -p ppi-benchmark/Experiments/APG/$ExpTyp/
cp xmlsplitter.py ppi-benchmark/Experiments/APG/$ExpTyp/xmlsplitter.py
cp run.py ppi-benchmark/Experiments/APG/$ExpTyp/run.py  ##
cd ppi-benchmark/Experiments
make experiment Corpora="DS" Kernel="APG" expType=$ExpTyp

if false
then

    # the main results are given in svn/ppi-benchmark/Experiments/APG/CV/DS.sql as well as in svn/ppi-benchmark/Experiments/APG/CV/predict/DS
    # upload the results from DS.sql to PostgreSQL:
    echo "uploading results to PostgreSQL ..."
    make output2db Corpora="DS" Kernel="APG" expType=$ExpTyp
    cd ..
    cd Database

    # assign fold IDs to the different parameter selections of each cross-validation run
    psql -h localhost -d ppi -U ppi -f manage_folds.sql
fi

#return to the start directory and show the time at which this pipeline ended
cd ../..
echo "calculation ended at " $(date +"%T")
