#    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>, Elham Abbasian <e_abbasian@yahoo.com>

#    This script executes the steps from the protein-protein-interaction pipeline of Tikk et al. (scripts/ppi-benchmark/Documentation/kernels-howto.pdf, (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).
#    The preprocessing steps were isolated as executable JAR files from the source code provided by Tikk et al. and partially modified to work with the compound-protein interaction files and the make-experiment steps. They generate the all-paths graph kernel-specific input format from the general XML format defined by Tikk et al. The general XML format can be built with the newly created script data_sets/DS1/annotatedsen_to_xml.py. The make-experiment steps contain 10-fold cross validation runs with different parameter selections and the uploading process of the results to a PostgreSQL database. Please, read the CPI-Pipeline documentation to find out how to configure the database and how to modifiy the configuration files before running this script.

# copy input files with the general XML format to the folder export_step1
cp generate_XML_files/DS1/DS1.xml CPI-corpora-preparing/export_step1/
cd CPI-corpora-preparing/export_step1/

# Step 1: extract all sentences from the XML file and enclose them in <s id>...</s> tags
# kernels-howto.pdf - Appendix C, Palaga’s Learning format API Java library
# Output: DS1.xml-ptb-s.txt
echo "step 1 ..."
java -jar preparing_parsing_input.jar -f DS1.xml 

# Step 2: build a syntactic tree parse with part-of-speech tags using the BLLIP reranking parser (also known as Charniak-Johnson parser, Charniak parser, Brown reranking parser) - https://github.com/BLLIP/bllip-parser
# Output: DS1.xml-ptb-s.txt-parsed.txt and -parsed.err
echo "step 2 ..."
cd ..
cp export_step1/DS1.xml-ptb-s.txt bllip-parser/
cd bllip-parser/
./parse.sh DS1.xml-ptb-s.txt > DS1.xml-ptb-s.txt-parsed.txt 2>DS1.xml-ptb-s.txt-parsed.err
# add the identifiers from the input file in each line of the current output file
# Output: DS1.xml-ptb-s.txt-parsed_modified.txt
# ToDo: include biomedical parsing model - debug (kernels-howto.pdf)
python merge_identifiers.py 
cd ..
mkdir export_step3/charniak-johnson/
cp bllip-parser/DS1.xml-ptb-s.txt-parsed_modified.txt export_step3/charniak-johnson/

# Step 3: merge BLLIP parser results with the XML file from step 1 in  <bracketings>...</bracketings> tags for each sentence
# the dependency parses and the tokenization with character offsets and part-of-speech tags will also be generated within this step
# Output: file DS1.xml.inj1
echo "step 3 ..."
cp export_step1/DS1.xml export_step3/
cd export_step3/
java -jar step_3_and_5_injection_lib.jar -f DS1.xml -p DS1.xml-ptb-s.txt-parsed_modified.txt -o DS1.xml.inj1 -i

# Step 4: alignment of the character offsets in the original sentence with the parsed results (<bracketings>...</bracketings>)
# Output: DS1.xml.inj1-bracketing-tokens.txt.
echo "step 4 ..."
cd ..
cp export_step3/DS1.xml.inj1 export_step4/
cd export_step4/
java -jar step_4_BracketingTokenMapper.jar DS1.xml.inj1 

# Step 5: injection of the aligned character offsets to the XML file DS1.xml.inj1 (<bracketings>...</bracketings>)e
# Output: DS1.xml.inj1.inj2
echo "step 5 ..."
cd ..
cp export_step4/DS1.xml.inj1-bracketing-tokens.txt step5_copied_from_3/
# ToDo: combine directories 3 and 5, because they use the same JAR file
cp export_step3/DS1.xml.inj1 step5_copied_from_3/
cd step5_copied_from_3
java -jar step_3_and_5_injection_lib.jar -f DS1.xml.inj1 -t DS1.xml.inj1-bracketing-tokens.txt -o DS1.xml.inj1.inj2

# Step 6: rename the file DS1.xml.inj1.inj2 to DS1.xml and (document-level) splitting of the sentences for 10-fold cross-validation (randomSplit.pl was slightly modified to generate the correct all-paths graph-specific format from the given input file - marked with "Kersten")
# Output: DS1/test-1 - DS1/test-2
echo "step 6 ..."
cd ..
cp step5_copied_from_3/DS1.xml.inj1.inj2 splitting
cd splitting
mv DS1.xml.inj1.inj2 DS1.xml
./randomSplit.pl DS1.xml 

## the cross-validation files need to be renamed and the folders that need to be copied to the directory ppi-benchmark as input files for the make-experiment steps will be prepared
## zip all cross-validation text files - test0.txt contains data to evaluate one of the ten parts and train0.txt contains the rest of the data for the training process
python ../../rename_files_splitting_DS1.py
cd ..
mkdir export_step6/splits-test-train
mkdir export_step6/splits-test-train/DS1
cp splitting/DS1/* export_step6/splits-test-train/DS1/
cp splitting/DS1.xml export_step6/
cd export_step6
java -jar split_AllGraphTransformer_CV.jar -f DS1.xml -s splits-test-train -o CV
echo "copying files ..."
cd CV/DS1
gzip *.txt

# return to the start directory and copy all files that are needed to run the all-paths graph kernel make-experiment steps
cd ../../../..
mkdir ppi-benchmark/Corpora/splits-test-train/
mkdir ppi-benchmark/Corpora/splits-test-train/DS1/
cp CPI-corpora-preparing/export_step6/splits-test-train/DS1/* ppi-benchmark/Corpora/splits-test-train/DS1/
mkdir ppi-benchmark/Corpora/APG/
mkdir ppi-benchmark/Corpora/APG/CV/
mkdir ppi-benchmark/Corpora/APG/CV/corpus/
cp -r CPI-corpora-preparing/export_step6/CV/DS1/ ppi-benchmark/Corpora/APG/CV/corpus/
mkdir ppi-benchmark/Corpora/Original/
cp CPI-corpora-preparing/export_step1/DS1.xml ppi-benchmark/Corpora/Original/
mkdir ppi-benchmark/Corpora/Original-Modified/
cp CPI-corpora-preparing/splitting/DS1.xml ppi-benchmark/Corpora/Original-Modified/

# start cross-validation experiments
echo "run APG pipeline ..."
cd ppi-benchmark/Experiments
make experiment Corpora="DS1" Kernel="APG" expType="CV"

# the main results are given in ppi-benchmark/Experiments/APG/CV/DS1.sql as well as in ppi-benchmark/Experiments/APG/CV/predict/DS1
# upload the results from DS1.sql to PostgreSQL:
echo "uploading results to PostgreSQL ..."
make output2db Corpora="DS1" Kernel="APG" expType="CV"
cd ..
cd Database

# assign fold IDs to the different parameter selections of each cross-validation run
psql -h localhost -d ppi -U ppi -f manage_folds.sql

#return to the start directory and show the time at which this pipeline ended
cd ../..
echo "calculation ended at " $(date +"%T")
