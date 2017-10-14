#    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>, Elham Abbasian <e_abbasian@yahoo.com>

#    This script executes the steps from the protein-protein-interaction pipeline of Tikk et al. (scripts/ppi-benchmark/Documentation/kernels-howto.pdf, (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).
#    The results of preprocessing steps from APG_pipeline_DS1.sh and APG_pipeline_DS2.sh were concatenated, copied, and used for this shell script. More details can be found in the project wiki.

# copy input files with the general XML format to the folder export_step1
cp generate_XML_files/DS3/DS3.xml CPI-corpora-preparing/export_step1/
cd CPI-corpora-preparing/export_step1/

# Step 1: extract all sentences from the XML file and enclose them in <s id>...</s> tags
# kernels-howto.pdf - Appendix C, Palaga’s Learning format API Java library
# Output: DS3.xml-ptb-s.txt
echo "step 1 ..."
java -jar preparing_parsing_input.jar -f DS3.xml 

# Step 2: build a syntactic tree parse with part-of-speech tags using the BLLIP reranking parser (also known as Charniak-Johnson parser, Charniak parser, Brown reranking parser) - https://github.com/BLLIP/bllip-parser
# Output: DS3.xml-ptb-s.txt-parsed.txt and -parsed.err
echo "step 2 ..."
cd ..
cp export_step1/DS3.xml-ptb-s.txt bllip-parser/
cd bllip-parser/
./parse.sh DS3.xml-ptb-s.txt > DS3.xml-ptb-s.txt-parsed.txt 2>DS3.xml-ptb-s.txt-parsed.err
# add the identifiers from the input file in each line of the current output file
# Output: DS3.xml-ptb-s.txt-parsed_modified.txt
# ToDo: include biomedical parsing model - debug (kernels-howto.pdf)
python merge_identifiers_3.py 
cd ..
cp bllip-parser/DS3.xml-ptb-s.txt-parsed_modified.txt export_step3/charniak-johnson/

# Step 3: merge BLLIP parser results with the XML file from step 1 in  <bracketings>...</bracketings> tags for each sentence
# the dependency parses and the tokenization with character offsets and part-of-speech tags will also be generated within this step
# Output: file DS3.xml.inj1
echo "step 3 ..."
cp export_step1/DS3.xml export_step3/
cd export_step3/
java -jar step_3_and_5_injection_lib.jar -f DS3.xml -p DS3.xml-ptb-s.txt-parsed_modified.txt -o DS3.xml.inj1 -i

# Step 4: alignment of the character offsets in the original sentence with the parsed results (<bracketings>...</bracketings>)
# Output: DS3.xml.inj1-bracketing-tokens.txt.
echo "step 4 ..."
cd ..
cp export_step3/DS3.xml.inj1 export_step4/
cd export_step4/
java -jar step_4_BracketingTokenMapper.jar DS3.xml.inj1 

# Step 5: injection of the aligned character offsets to the XML file DS3.xml.inj1 (<bracketings>...</bracketings>)e
# Output: DS3.xml.inj1.inj2
echo "step 5 ..."
cd ..
cp export_step4/DS3.xml.inj1-bracketing-tokens.txt step5_copied_from_3/
# ToDo: combine directories 3 and 5, because they use the same JAR file
cp export_step3/DS3.xml.inj1 step5_copied_from_3/
cd step5_copied_from_3
java -jar step_3_and_5_injection_lib.jar -f DS3.xml.inj1 -t DS3.xml.inj1-bracketing-tokens.txt -o DS3.xml.inj1.inj2

# Step 6: rename the file DS3.xml.inj1.inj2 to DS3.xml and (document-level) splitting of the sentences for 10-fold cross-validation (randomSplit.pl was slightly modified to generate the correct all-paths graph-specific format from the given input file - marked with "Kersten")
# Output: DS3/test-1 - DS3/test-2
echo "step 6 ..."
cd ..
cp step5_copied_from_3/DS3.xml.inj1.inj2 splitting
cd splitting
mv DS3.xml.inj1.inj2 DS3.xml
./randomSplit.pl DS3.xml 

# the cross-validation files need to be renamed and the folders that need to be copied to the directory ppi-benchmark as input files for the make-experiment steps will be prepared
# zip all cross-validation text files - test0.txt contains data to evaluate one of the ten parts and train0.txt contains the rest of the data for the training process
# read old cross-validation parts (PubMed IDs) and merge them with new data set identifiers of DS3
python ../../rename_files_splitting_DS3.py
cd ../..
python merge_splitting_DS3.py
cd CPI-corpora-preparing
cp -r splitting/DS3/ export_step6/splits-test-train
cp splitting/DS3.xml export_step6/
cd export_step6
java -jar split_AllGraphTransformer_CV.jar -f DS3.xml -s splits-test-train -o CV
echo "copying files ..."
cd CV/DS3
gzip *.txt

# return to the start directory and copy all files that are needed to run the all-paths graph kernel make-experiment steps
cd ../../../..
cp -r CPI-corpora-preparing/export_step6/splits-test-train/DS3/ ppi-benchmark/Corpora/splits-test-train/
cp -r CPI-corpora-preparing/export_step6/CV/DS3/ ppi-benchmark/Corpora/APG/CV/corpus/
cp CPI-corpora-preparing/export_step1/DS3.xml ppi-benchmark/Corpora/Original/
cp CPI-corpora-preparing/splitting/DS3.xml ppi-benchmark/Corpora/Original-Modified/

# start cross-validation experiments
echo "run APG pipeline ..."
cd ppi-benchmark/Experiments
make experiment Corpora="DS3" Kernel="APG" expType="CV"

# the main results are given in svn/ppi-benchmark/Experiments/APG/CV/DS3.sql as well as in svn/ppi-benchmark/Experiments/APG/CV/predict/DS3
# upload the results from DS3.sql to PostgreSQL:
echo "uploading results to PostgreSQL ..."
make output2db Corpora="DS3" Kernel="APG" expType="CV"
cd ..
cd Database

# assign fold IDs to the different parameter selections of each cross-validation run
psql -h localhost -d ppi -U ppi -f manage_folds.sql

#return to the start directory and show the time at which this pipeline ended
cd ../..
echo "calculation ended at " $(date +"%T")
