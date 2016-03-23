#    Copyright (c) 2015, Kersten Doering <kersten.doering@gmail.com>

#    This script executes the steps from the protein-protein-interaction pipeline of Tikk et al. (scripts/ppi-benchmark/Documentation/kernels-howto.pdf, (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).
#    In case of the shallow linguistic kernel approach, only the syntactic tree parse is needed, which will be generated within the first make-experiment step. To compare this method with the all-paths graph kernel approach, the cross-validation files are copied from the all-path graph kernel folder. Alternatively, these files can be copied from their original directories as used in the script APG_pipeline_DS1.sh.
#    The make-experiment steps contain 10-fold cross validation runs with different parameter selections and the uploading process of the results to a PostgreSQL database. Please, read the CPI-Pipeline documentation to find out how to configure the database and how to modifiy the configuration files before running this script.

# change into the (just prepared folders from the all-paths graph kernel directory)
cd ppi-benchmark/Corpora/Original
# ToDo: use copy command to get files from generate_XML_files
cp DS1.xml ../Original-Modified 
cd ..
# if there are files from a previous shallow linguistic kernel run, they will be removed 
rm Splits/DS1/*
cp splits-test-train/DS1/* Splits/DS1/
cd Splits
# rename the files in the direcotry Splits
# remove the PubMed ID in front of each document ID in all text files
# this format was needed in case of the all-path graph kernel approach
python modify.py
python rename_files_splitting_DS1_again.py
# change into directory Experiments to start the calculation and the upload process
cd ../../Experiments
echo "run SL pipeline ..."
make experiment Corpora="DS1" Kernel="SL" expType="CV"
echo "uploading results to PostgreSQL ..."
make output2db Corpora="DS1" Kernel="SL" expType="CV"
cd ..
cd Database
psql -h localhost -d ppi -U ppi -f manage_folds.sql
#return to the start directory and show the time at which this pipeline ended
cd ../..
echo "calculation ended at " $(date +"%T")
