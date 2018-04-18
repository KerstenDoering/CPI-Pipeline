Compound-Protein Interaction Pipeline
=====================================


Introduction
************

- The presented pipeline uses the protein-protein interaction benchmark package published by Tikk et al. (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).

- The selection of considered kernels and software components was reduced to the all-paths graph (APG) kernel and the shallow linguistic (SL) kernel, because they performed best on the protein-protein interaction (PPI) data sets.

- In this project, the two kernels were applied to two compound-protein interaction (CPI) in PubMed sentences.

- The complete data set consists of 2753 sentences. Within these sentences, 3724 compound-protein pairs were annotated to show a functional relationship and 2672 compound-protein pairs were marked as no-interaction pairs.

- We consider co-occurences as an approach to predict every appearance of a compound and a protein in a sentence as a functional relationship (recall 100%, specificity 0%) and call it the baseline calculation, taking into account the number of true functional relationships.

- From the given numbers, the data set shows an precision (equal to accuracy in this case) of 58.2 % and an F1 score of 73.6 %.

- APG and SL kernel both perform better than the concept of co-occurrences as shown in the following tables.

- SL kernel results:

    .. image:: figures/APG_DS.png

- APG kernel results:

    .. image:: figures/SL_DS.png

Functional relationships with and without an enclosed interaction verb
######################################################################

- The whole prediction can be further divided into considering only pairs of compounds and proteins which enclose an interaction verb (data set 1 - DS1) and pairs of compounds and proteins that do show this sentence structure (data set 2 - DS2).

- These verbs have been defined in the publication of the web service prolific (Senger and Grüning et al., 2012. Mining and evaluation of molecular relationships in literature. Bioinformatics).

- The following table shows the evaluation of the co-occurrences approach (DS - Data set, Sent. - Sentences, Sens. - Sensitivity, Spec. - Specificity, Prec. - Precision, Acc. - Accuracy, F1 - F1 score, evaluation parameters shown in percent):

    .. image:: figures/co-occurrences.png

- The next table shows the results of the APG kernel pipeline for DS1 and DS2:

    .. image:: figures/APG.png

- The last table shows the results of the SL kernel pipeline for DS1 and DS2:

    .. image:: figures/SL.png

- The ratio of sentences with and without interaction verbs for the complete PubMed data set is around 40 % DS1 and 60 % DS2, based on an analysis with PubMedPortable.

- In the case of DS1 and DS2, the percentages are 45.7 % (1259/(1259+1494)) and 54.3 % (1494/(1259+1494)).

- Considering the manual curation of false positives resulting from the automatic named entity recognition process, the empirical ratios can be considered as similar.

The benchmark data set creation
###############################

- The data sets were created by selecting the first 40,000 PubMed abstracts from 2009 with PubMedPortable (https://github.com/KerstenDoering/PubMedPortable).

- The chemical compounds were identified with the backend of prolific using the Hettne rules (Hettne et al., 2009. A dictionary to identify small molecules and drugs in free text. Bioinformatics).

- The web service Whatizit was used for gene and protein synonyms (Rebholz-Schuhmann,D. et al., 2008. Text processing through Web services: calling Whatizit. Bioinformatics).

- After automated extraction of all sentences with an interaction verb (first 20,000 abstracts for DS1) and without an interaction enclosed by two biomolecues (second 20,000 abstracts for DS2), they were displayed in HTML pages with Javascript buttons to select a status for each sentence.

- If a sentence contained at least one interacting pair of biomolecules, the status "Interaction" was selected for this sentence. The alternative was "No Interaction".

- If the named entity recognition tools tagged false positive synonyms, they were annotated in the separate file RM_comments.csv.

- If there were non-interacting molecules in a sentence with the status "Interaction", they were also annotated in the separate CSV table.

- If every molecule in the sentence was a false positive named entity, the status of the sentence was set to "False positive example".

- The data set curation was done by Michael Becer, supervised by Kersten Döring.

- All potentially functional interaction pairs marked as false positives were not considered in the evaluation process of the two kernel approaches.

- More information about the theoretical background of the kernels, the data sets, and other related information can be found in Kersten Döring's Dissertation (https://www.freidok.uni-freiburg.de/data/10565).

    - The SL kernel results contained in this thesis are not the results presented here, because they were generated with a customised pipeline, independently from the ppi-benchmark package.

    - The PubMedPortable project is referred to as PubMed2Go in this thesis.

Technical background of the XML data set
########################################

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


Technical Requirements for running APG and SL Kernel Pipeline
*************************************************************

- Many of the following steps are described similarly in the original ppi-benchmark documentation (scripts/ppi-benchmark/documentationkernels-howto.pdf).


Required Installation Packages
##############################

- The operating system for the CPI-pipeline was Ubuntu 14.04 LTS and the whole pipeline was tested with Ubuntu 16.04 LTS.

- All packages can be installed with "apt-get install", Synaptic Package Manager, or the new Ubuntu Software Center.

- List of packages:

    - postgresql (here: version 9.3, used to store evaluation results)

    - libxml-perl (here: version 0.08, used for the generation of cross-validation splits)

    - python-numpy (here: using Python 2.7, used within the make experiment steps)

    - default-jdk (Java 7 or 8, used for the execution of JAR files)

    - python-nltk


Makefile Configuration
######################

- There are many Makefile parameters which are automatically set by using the correct make commands, as described in the section "How to run the Kernel Pipelines".

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

- If you do not want to insert your password everytime to connect to a PostgreSQL database, use these commands (recommended):

    - touch ~/.pgpass

    - chmod 600 ~/.pgpass

    - cat >> ~/.pgpass <<EOF

        - localhost:*:ppi:ppi:ppi

        - EOF

- Create the tables which are needed for uploading the results. Change into scripts/ppi-benchmark/Database and execute the following command:

    - psql -h localhost -d ppi -U ppi -f init-ppiCV.sql 


How to run the Kernel Pipelines
*******************************

- This section describes how to use run the APG and SL kernel with the combined data set (DS), DS1, and DS2 in different modes:

    - CV: 10x-cross-validation

    - PR: prediction, based on the trained model of the combined data set (DS) 

    - XX: cross-corpus training and prediction on user-specific data sets

- Furthermore, it contains a short paragraph about how to use these models.

APG Kernel pipeline
###################

- These are the 3 main commands:
 
    - CV: make experiment Kernel=APG expTyp=CV InputFile=DS.xml Processors=4
 
    - PR: make experiment Kernel=APG expTyp=PR InputFile=DS.xml Processors=4
 
    - XX: make experiment Kernel=APG expTyp=XX TrainFile=train.xml TestFile=test.xml Processors=4

- You can use the test data set DS-40.xml with 40 sentences to check whether your pipeline works. 

- While the complete DS1 pipeline runs around 3:15 h the test case takes only a few minutes on a notebook with an Intel Core i7-6700HQ (4x 2,6 GHz).

- To use this test data set, go to your (new) working directory into "scripts" and run one of the given make commands with a data set from the folder "scripts/generate_XML_files/DS", e.g.:

    - make experiment Kernel=APG expTyp=PR InputFile=annotate_res.xml Processors=4

- The make command also uploads the results to the PostgreSQL database. 

- You can clean your APG workspace after a calculation is finished:

    - make clean-APG

- Or you can clean the whole workspace:

    - make clean-all

- Elham Abbasian was involved in creating the shell script for this pipeline as part of her Master Thesis, supervised by Kersten Döring.

- Ammar Qaseem updated and completely refined the first version of this pipeline to be used in three modes (cross-validation, prediction, cross-corpus) with only one script APG_Pipeline.sh.

- The threshold for a positive or negative prediction is optimized for the highest F1 score and stored in the SQL database.

- In "scripts/ppi-benchmark/Experiments/APG/PR/predict/DS/train0000/predict1.out", you will find the test predictions with the original class in the second column and the complete sentence identifier in the first column (for the lambda value 1).

- In "scripts/ppi-benchmark/Experiments/APG/PR/predict/DS/train0000/threshold1.out", you will find the train predictions (self-prediction) for the F1 score optimization with the original class in the second column and the complete sentence identifier in the first column (for the lambda value 1).

- The file scripts/ppi-benchmark/Experiments/APG/PR/DS.sql contains all prediction values (0 for false, and 1 for true, and the prediction value itself).

SL Kernel pipeline
##################

- These are the 3 main commands:
 
    - CV: make experiment Kernel=SL expTyp=CV InputFile=DS.xml Processors=4
 
    - PR: make experiment Kernel=SL expTyp=PR InputFile=DS.xml Processors=4
 
    - XX: make experiment Kernel=SL expTyp=XX TrainFile=train.xml TestFile=test.xml Processors=4

- You can clean your APG workspace after a calculation is finished:

    - make clean-SL

- Or you can clean the whole workspace:

    - make clean-all

- Ammar Qaseem updated and completely refined the first version of this pipeline to be used in three modes (cross-validation, prediction, cross-corpus) with only one script SL_Pipeline.sh.

- Michael Becer was involved in developing a previous version of an independently customized pipeline using the SL kernel as part of his Bachelor Thesis, supervised by Kersten Döring.

- Kevin Selm wrote a bugfix for the jSRE software, because it was not possible to use different parameter selections of n and w. 

    - Original software link: 

        - https://hlt-nlp.fbk.eu/technologies/jsre

- The ppi-benchmark pipeline was changed to make use of the JAR file scripts/ppi-benchmark/Kernels/jsre/source/dist/runTrain.jar, which was exported from a newly created Eclipse project with the source code of the original software and the debugged code of Kevin Selm.

    - You can find these files in the folder scripts/jSRE_debug.

- The complete DS1 pipeline runs in around 0:12 h with an Intel Core i7-6700HQ (4x 2,6 GHz).

- The threshold for a positive or negative prediction is zero and stored in the SQL database.


- In "scripts/ppi-benchmark/Experiments/SL/PR/predict/DS/train0000/predictn=3w=1.out", you will find the predictions with the original class in the second column and the complete sentence identifier in the first column (for n=3 and w=1).

- The file scripts/ppi-benchmark/Experiments/SL/PR/output.sql contains all prediction values (0 for false, and 1 for true, and the prediction value itself).

Data set evaluation
###################

- The folder results/summary/APG/output/ contains scripts to evaluate the results (numbers shown in the tables in the section "Introduction").

- If you want to repeat the evaluation procedure, execute the following steps:

    - Remove all files in the folder output, except average.py and header.py.

    - ./get_csv_results.sh

    - Change into the directory output.

    - python average.py

    - cat DS1*average.csv > DS1_average.csv

    - cat DS2*average.csv > DS2_average.csv

    - python header.py

    - Check the files DS1_average_header.csv and DS2_average_header.csv. They exist as a backup in the folder results/summary/APG/final/ and the selected SQL results are stored as a backup in the folder results/summary/APG/backup_original.

- These are the steps to get the originally combined data set evaluation result tables:

    - APG results:

        - ./get_csv_results.sh

        - change into directory output

        - python average.py

        - cat DS3*average.csv > DS3_average.csv

        - python header.py

    - SL results:

        - change into directory /CPI-Pipeline/results/summary/DS3/jSRE

        - python generate_selects_psql.py

        - ./get_csv_results.sh 

        - change into directory output

        - python average.py 

        - cat DS3*average.csv > DS3_average.csv

        - python header.py 


- You can reproduce any APG cross-validation run by commenting out lines 187, 191, 192, and 198 and copying your selected cross-validation splits to CPI-corpora-preparing/splitting/DS.

- You can reproduce any SL cross-validation run by commenting out lines 197-199 in scripts/ppi-benchmark/Corpora/Makefile and line 90 in scripts/SL_Pipeline.sh (and copying your selected cross-validation splits to CPI-corpora-preparing/splitting/DS).

Usage of Created Models
#######################

- If you want to use the models created with any data set, use the XX mode. If you want to use our representative model of PubMed, run the PR mode.

- You can use PubMedPortable with its named entity recognition interfaces to prepare sentences with highlighted compounds and proteins.

- The basic input for the script annotatedsen_to_xml.py (training_dataset_sorted.csv) can be created by generating a tab-separated format which contains the following columns:

    - PubMed ID

    - Sentence with XML tags for all named entities

    - As many more columns as there are pairs of related entities

        - Format of each pair: <entity>__<entity>__<interaction>

- This format will automatically generated with the following example command in the folder "scripts/annotate_entities":

    - make annotate InputFile=inp/pmid_example OutputFile=annotate_res.txt Processors=2

- You will need to configure python-nltk to download the punkt tokenizer before:

    - cd ~

    - mkdir nltk_data

    - ipython

    - import nltk

    - nltk.download_shell()

    - d

    - punkt

    - q

- The example output of this file, converted to an XML file (with the script annotatedsen_to_xml.py as described in the section "Technical background of the XML data set") is "scripts/generate_XML_files/DS/annoate_res.xml".

- Considering the output of such an experiment, all positively predicted pairs of entities can be used for an ongoing analysis, e.g. in the process of filtering out interaction partners from large-scale corpora.

- If you want to run your own models in the PR mode, you need to copy files from your XX run to specific directories.

- In the case of the SL kernel, you need to copy the .model file from "scripts/ppi-benchmark/Experiments/SL/XX/trained/DS/train0" to "scripts/training_model/SL_PR_training/trained_model/DS/train0".

- In the case of the APG kernel, there are more steps:

    - Copy your .model file from "scripts/ppi-benchmark/Experiments/APG/PR/trained/DS/train0" to "scripts/training_model/APG_PR_training/trained_model/DS/train0".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/corpus/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/Corpus_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/dictionary/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/Dict_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/linearized/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/Linearized_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/normalized/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/Norm_train0.txt.gz".


Contact
*******

- Please, write an e-mail, if you have questions, feedback, improvements, or new ideas:

    - kersten.doering@gmail.com

    - ammar.qaseem@pharmazie.uni-freiburg.de

- If you are interested in related projects, visit our working group's homepage:

    - http://www.pharmaceutical-bioinformatics.de


License
#######

- The CPI-Pipeline project is published with an ISC license given in "license.txt".
