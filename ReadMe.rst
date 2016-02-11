Compound-Protein Interaction Pipeline
=====================================


Introduction
************

- The presented pipeline uses the protein-protein interaction benchmark package published by Tikk et al. (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).

- The selection of considered kernels and software components was reduced to the all-paths graph (APG) kernel and the shallow linguistic (SL) kernel, because they performed best on the protein-protein interaction (PPI) data sets.

- The two kernels were applied to two compound-protein interaction (CPI) data sets. 

    - Data set 1 (DS1) consists of sentences in which an interaction verb is enclosed by a protein and a chemical compound.

    - In the case of data set 2 (DS2), two biomolecules do not enclose such an interaction verb.

    - These verbs have been defined in the publication of the web service prolific (Senger and Grüning et al., 2012. Mining and evaluation of molecular relationships in literature. Bioinformatics).

- The data sets were created by selecting the first 40,000 PubMed abstracts from 2009 with PubMedPortable (https://github.com/KerstenDoering/PubMedPortable).

    - The chemical compounds were identified with the backend of prolific using the Hettne rules (Hettne et al., 2009. A dictionary to identify small molecules and drugs in free text. Bioinformatics).

    -  The web service Whatizit was used for gene and protein synonyms (Rebholz-Schuhmann,D. et al., 2008. Text processing through Web services: calling Whatizit. Bioinformatics).

- After automated extraction of all sentences with an interaction verb (first 20,000 abstracts for DS1) and without an interaction enclosed by two biomolecues (second 20,000 abstracts for DS2), they were displayed in HTML pages with Javascript buttons to select a status for each sentence.

    - If a sentence contained at least one interacting pair of biomolecules, the status "Interaction" was selected for this sentence. The alternative was "No Interaction".

    - If the named entity recognition tools tagged false positive synonyms, they were annotated in the separate file RM_comments.csv.

    - If there were non-interacting molecules in a sentence with the status "Interaction", they were also annotated in the separate CSV table.

    - If every molecule in the sentence was a false positive named entity, the status of the sentence was set to "False positive example".

    - The data set curation was done by Michael Becer, supervised by Kersten Döring.

    - All potentially functional interaction pairs marked as false positives were not considered in the evaluation process of the two kernel approaches.

- The number of compounds and proteins co-occurring in sentences compared to the number of true functional relationships can be considered as the baseline, stating how many positive interactions can be expected by using the concept of co-occurrences on PubMed sentences in general. 

    - The following table shows the evaluation of the co-occurrences approach (DS - Data set, Sent. - Sentences, Sens. - Sensitivity, Spec. - Specificity, Prec. - Precision, Acc. - Accuracy, F1 - F1 score, evaluation parameters shown in percent):

    .. image:: figures/co-occurrences.png

    - If each relationship is predicted to be positive, the sensitivity is 100 % and the specificity is 0 %, because there are no true negative predictions. 

    - For this reason, the precision is equal to the accuracy value in this special case.

- More information about the theoretical background of the kernels, the data sets, and other related information can be found in Kersten Döring's Dissertation (https://www.freidok.uni-freiburg.de/data/10565).

    - The SL kernel results contained in this thesis are not the results presented here, because they were generated with a customised pipeline, independently from the ppi-benchmark package.

    - The PubMedPortable project is referred to as PubMed2Go in this thesis.


XML Data Set Creation
*********************

- The script parser.py in the directories scripts/generate_XML_files/DS1/ und scripts/generate_XML_files/DS2 creates the files interactions.txt and no_interactions.txt from the HTML files in the folder data_sets. 

    - The names of these files refer to the basic status of all sentences inside the text file.

    - Relationship_Mining_10000.html and Relationship_Mining_20000.html were concatenated to the file Relationship_Mining.html resulting in DS1. The other two HTML files represent DS2.

- The script get_relations.py in the directories scripts/generate_XML_files/DS1/ und scripts/generate_XML_files/DS2 processes the files interaction.txt and no_interaction.txt using the (concatenated) file RM_comments.csv with annotations of false positive compounds (FP-C), false positive proteins (FP-P), non-interacting compounds (NI-C), and non-interacting proteins (NI-P).

    - The ouptut of get_relations.py is the file training_dataset.txt.

    - This file can be sorted by PubMed IDs with the command "sort -u training_dataset.txt > training_dataset_sorted.csv", individually done with DS1 and DS2.

- The script annotatedsen_to_xml.py generates the files DS1.xml and DS2.xml, building a unified XML format described by Tikk et al.

    - This script was developed by Elham Abbasian in her Master Thesis, supervised by Kersten Döring.

- The SL kernel implementation in the ppi-benchmark package of Tikk et al. worked with this XML format, but the preprocessing for the APG kernel-required format did not work straight forward. Therefore, the single steps described in their documentation appendix (here: scripts/ppi-benchmark/documentationkernels-howto.pdf) were isolated from the available source code and stored as executable JAR files in the folder scripts/CPI-corpora-preparing with Eclipse.

- The XML files can be checked for consistency. Furthermore, it can be seen how many documents (PubMed IDs) and sentences there are:

    java -jar ConsistencyChecker.jar DS1/DS1.xml 

        INFO: Processing 'DS1/DS1.xml'...

        Processing corpus 'DS1' ...

        Documents seen: 830

        Sentences seen: 1259


    java -jar ConsistencyChecker.jar DS2/DS2.xml 

        INFO: Processing 'DS2/DS2.xml'...

        Processing corpus 'DS1' ...

        processed 1000 docs (2155.1724 docs/sec)

        Documents seen: 1066

        Sentences seen: 1494


    java -jar ConsistencyChecker.jar DS1_40/DS1.xml 

        INFO: Processing 'DS1_test_case_40_sentences/DS1.xml'...

        Processing corpus 'DS1' ...

        Documents seen: 26

        Sentences seen: 40


APG Kernel Pipeline
*******************

- Many of the following steps are described similarly in the original ppi-benchmark documentation (scripts/ppi-benchmark/documentationkernels-howto.pdf).


Required Installation Packages
##############################

- The operating system for the CPI-pipeline was Ubuntu 14.04 LTS.

- All packages can be installed with "apt-get install", Synaptic Package Manager, or the new Ubuntu Software Center.

- List of packages:

    - postgresql (here: version 9.3, used to store evaluation results)

    - libxml-perl (here: version 0.08, used for the generation of cross-validation splits)

    - python-numpy (here: using Python 2.7, used within the make experiment steps)

    - default-jdk (here: Java 7, used for the execution of JAR files)


Makefile Configuration
######################

- The pipeline needs to be configured for the usage of DS1 or DS2 and the application of the APG or SL kernel.

- To run the pipeline with APG and DS1 a few changes were made in comparision to the original configuration of the ppi-benchmark package (the "#" character comments out lines of code).

- The file "scripts/ppi-benchmark/Experiments/APG/Makefile" has got the following configuration, now:

    # Produced by the pipeline

    TOKENIZER=Charniak-Lease

    PARSER=Charniak-Johnson-McClosky

- To make use of DS1 and APG with cross-validation, the following lines need to be set in the file "scripts/ppi-benchmark/Makefile.config":

    BENCHMARKCORPORA=DS1 #DS2 #LLL #HPRD50 AIMed BioInfer IEPA


    CORPORA=$(BENCHMARKCORPORA)

    TEST_CORPORA=DS1 #DS2 #LLL HPRD50


    KERNELS=APG #SL #ST SST PT SpT kBSPS APG cosine edit SL Kim

    EXPTYPES=CV# CC CL


PostgreSQL Configuration
########################

- Set your own user to be a PostgreSLQ superuser after installation of the default package "postgresql".

    - Follow the instructions here:

        https://github.com/KerstenDoering/PubMedPortable/blob/master/documentation/quick_install.rst#creation-of-postgresql-superuser

- Type in the following commands to create a new user "ppi".

    - sudo useradd ppi -s /bin/false

    - sudo passwd ppi

    - sudo su -c "psql" postgres

        - CREATE USER ppi WITH PASSWORD 'ppi';

        - CREATE DATABASE ppi;

        - GRANT ALL PRIVILEGES ON DATABASE ppi TO ppi;

        - CREATE LANGUAGE plpgsql;

        - \\q

- If you do not want to insert your password everytime to connect to a PostgreSQL database, use these commands:

    - touch ~/.pgpass

    - chmod 600 ~/.pgpass

    - cat >> ~/.pgpass <<EOF

        - localhost:*:ppi:ppi:ppi

        - EOF


Executable Files
################

- If the following files are not executable after cloning this repository, make them executable with the command "sudo chmod +x <file>"

    - scripts/APG_pipeline_DS1.sh

    - scripts/APG_pipeline_DS2.sh

    - scripts/SL_pipeline_DS1.sh

    - scripts/SL_pipeline_DS1.sh

    - scripts/CPI-corpora-preparing/bllip-parser/first-stage/PARSE/parseIt

    - scripts/CPI-corpora-preparing/bllip-parser/second-stage/programs/features/best-parses

    - scripts/ppi-benchmark/Parsing/Charniak-Lease-2006Aug-reranking-parser/reranking-parser/first-stage/PARSE/parseIt

    - scripts/ppi-benchmark/Parsing/Charniak-Lease-2006Aug-reranking-parser/reranking-parser/second-stage/programs/features/best-parses

    - results/summary/jSRE/get_csv_results.sh

    - results/summary/APG/get_csv_results.sh

Run the APG Kernel Pipeline
###########################

- It is recommended that the folders CPI-corpora-preparing, generate_XML_files, and ppi-benchmark are copied with the shell scripts APG_pipeline_DS1.sh and APG_pipeline_DS2.sh to another directory to store these empty versions as a backup.

    - The path to the folder from which the pipeline should be executed needs to be set in the file "scripts/ppi-benchmark/Makefile.config" in line 7, e.g. like this:

    - baseDir=/home/<user>/Desktop/ppi-benchmark

- If the pipeline for DS2 should be run, the configuration needs to be updated as previously described in the subsection "Makefile Configuration".

- You can use the test data set with 40 sentences to check whether your pipeline works. 

- While the complete DS1 and DS2 runtime is about several hours, the test case takes around 6 min on a notebook with an Intel Core i7-6700HQ (4x 2,6 GHz).

    - To use this test data set, go to your (new) working directory and change into the folder scripts/generate_XML_files/DS1_test_case_40_sentences to copy the file DS1.xml into the directory scripts/generate_XML_files/DS1.

- Start the pipeline by executing the shell script in the command-line:

    - ./APG_pipeline_DS1.sh

    - The script contains more comments on the different preprocessing and make experiment steps.

    - The runtime can be checked considering the time written to the command-line before the script terminates.

- This script also uploads the results to the PostgreSQL database. 

- The folder results/summary/APG/output/ contains scripts to evaluate the results.

- If you want to repeat the evaluation procedure, execute the following steps:

    - Remove all files in the folder output, except average.py and header.py.

    - ./get_csv_results.sh

    - Change into the directory output.

    - python average.py

    - cat DS1*average.csv > DS1_average.csv

    - cat DS2*average.csv > DS2_average.csv

    - python header.py

    - Check the files DS1_average_header.csv and DS2_average_header.csv. They exist as a backup in the folder results/summary/APG/final/ and the selected SQL results are stored as a backup in the folder results/summary/APG/backup_original.

- The following table shows the results of the APG kernel pipeline for DS1 and DS2 (DS - Data set, Sent. - Sentences, Sens. - Sensitivity, Spec. - Specificity, Prec. - Precision, Acc. - Accuracy, F1 - F1 score, AUC - Area under the curve, evaluation parameters shown in percent):

    .. image:: figures/APG.png

- Elham Abbasian was involved in creating the shell script for this pipeline as part of her Master Thesis, supervised by Kersten Döring.

SL Kernel pipeline
******************

- The SL kernel pipeline can be started as described previously for the APG kernel pipeline.

- The Makefile line defining to use the APG kernel needs to be changed to make use of the SL kernel ("scripts/ppi-benchmark/Makefile.config"):

    - KERNELS= SL #APG #ST SST PT SpT kBSPS APG cosine edit SL Kim

- With the current implementation, the scripts SL_pipeline_DS1.sh and SL_pipeline_DS2.sh make use of the files generated in the first preprocessing steps of the APG pipeline.

- Copy them to the directory, in which you started your APG kernel calculation.

- If you did not yet run the APG kernel pipeline, open the scripts APG_pipeline_DS1.sh and APG_pipeline_DS2.sh, comment out the make experiment steps, and execute them as described in the previous section.

- The SL kernel pipeline does not need the dependency tree format and it makes use of the ppi-benchmark integrated Charniak-Lease package, but it needs the same cross-validation files to be directly comparable to the APG kernel approach.

- You can use the same directory to execute the SL kernel scripts as you did in case of the APG kernel approach, because the two kernels use different directories:

    - ./SL_pipeline_DS1.sh

    - ./SL_pipeline_DS2.sh

- The evaluation steps are very similar to the ones used for the APG kernel pipeline.

    - Execute the scripts in results/summary/jSRE as described in the previous section.

- These are the SL kernel pipeline results for DS1 and DS2 (DS - Data set, Sent. - Sentences, Sens. - Sensitivity, Spec. - Specificity, Prec. - Precision, Acc. - Accuracy, F1 - F1 score, AUC - Area under the curve, evaluation parameters shown in percent):

    .. image:: figures/SL.png

- Michael Becer was involved in developing a previous version of an independently customized pipeline using the SL kernel as part of his Bachelor Thesis, supervised by Kersten Döring.

- Kevin Selm wrote a bugfix for the jSRE software, because it was not possible to use different parameter selections of n and w. 

    - Original software link: 

        - https://hlt-nlp.fbk.eu/technologies/jsre

- The ppi-benchmark pipeline was changed to make use of the JAR file scripts/ppi-benchmark/Kernels/jsre/source/dist/runTrain.jar, which was exported from a newly created Eclipse project with the source code of the original software and the debugged code of Kevin Selm.

    - You can find these files in the folder scripts/jSRE_debug.


Usage of Created Models
***********************

- If you want to use the models created with DS1 or DS2, go to the folders scripts/ppi-benchmark/Experiments/APG/CV or scripts/ppi-benchmark/Experiments/SL/CV and comment out the training process step in run.py.

- You can use PubMedPortable with its named entity recognition interfaces to prepare sentences with highlighted compounds and proteins.

- The basic input for the script annotatedsen_to_xml.py (training_dataset_sorted.csv) can be created by generating a tab-separated format which contains the following columns:

    - PubMed ID

    - Sentence with XML tags for all named entities

    - As many more columns as there are pairs of related entities

        - Format of each pair: <entity>__<entity>__<interaction>

- Considering the output of such an experiment, all positively predicted pairs of entities can be used for an ongoing analysis, e.g. in the process of filtering out interaction partners from large-scale corpora.


Contact
*******

- Please, write an e-mail, if you have questions, feedback, improvements, or new ideas:

    - kersten.doering@gmail.com

- If you are interested in related projects, visit our working group's homepage:

    - http://www.pharmaceutical-bioinformatics.de


License
#######

- The CPI-Pipeline project is published with an ISC license given in "license.txt".
