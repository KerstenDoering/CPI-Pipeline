Compound-Protein Interaction Pipeline
=====================================


Introduction
************

- The presented pipeline uses the protein-protein interaction benchmark package published by Tikk et al. (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).

- The selection of considered kernels and software components was reduced to the all-paths graph (APG) kernel and the shallow linguistic (SL) kernel, because they performed best on the protein-protein interaction (PPI) data sets.

- In this project, the two kernels were applied to two compound-protein interaction (CPI) in PubMed sentences.

- The complete data set consists of 2613 sentences. Within these sentences, 2931 compound-protein pairs were annotated to show a functional relationship and 2631 compound-protein pairs were marked as no-interaction pairs.

- We consider co-occurences as an approach to predict every appearance of a compound and a protein in a sentence as a functional relationship (recall 100%, specificity 0%) and call it the baseline calculation, taking into account the number of true functional relationships.

- From the given numbers, the data set shows an precision (equal to accuracy in this case) of 52.7 % and an F1 score of 69.0 %.

- APG and SL kernel both perform better than the concept of co-occurrences as shown in the following tables.

- APG kernel results for CPI-DS dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - Param.
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 0.25
          - 81.7
          - 71.8
          - 76.6
          - 77.1
          - 79.0
          - 84.6

        * - 0.50
          - 82.7
          - 70.2
          - 75.8
          - 76.9
          - 79.0
          - 84.6

        * - 1.00
          - 81.4
          - 72.0
          - 76.6
          - 77.0
          - 78.8
          - 84.4

        * - 2.00
          - 79.7
          - 73.2
          - 77.0
          - 76.7
          - 78.2
          - 84.1


- SL kernel results for CPI-DS dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - n
          - w
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 1
          - 1
          - 76.6
          - 69.8
          - 74.0
          - 73.4
          - 75.2
          - 80.7

        * - 1
          - 2
          - 85.1
          - 61.0
          - 71.1
          - 73.8
          - 77.4
          - 80.5

        * - 1
          - 3
          - 87.2
          - 56.3
          - 69.1
          - 72.6
          - 77.0
          - 80.3

        * - 2
          - 1
          - 78.5
          - 70.8
          - 75.1
          - 74.9
          - 76.7
          - 81.8

        * - 2
          - 2
          - 85.6
          - 62.7
          - 72.1
          - 74.8
          - 78.2
          - 81.5

        * - 2
          - 3
          - 87.0
          - 59.8
          - 70.9
          - 74.2
          - 78.1
          - 81.3

        * - 3
          - 1
          - 79.5
          - 70.2
          - 75.0
          - 75.2
          - 77.2
          - 82.5

        * - 3
          - 2
          - 86.6
          - 62.8
          - 72.4
          - 75.5
          - 78.8
          - 82.2

        * - 3
          - 3
          - 87.3
          - 60.0
          - 71.1
          - 74.5
          - 78.3
          - 82.1

Functional relationships with and without an enclosed interaction verb
######################################################################

- The whole prediction can be further divided into considering only pairs of compounds and proteins which enclose an interaction verb (CPI-DS_IV) and pairs of compounds and proteins that don't show this sentence structure (CPI-DS_NIV).

- These verbs have been defined in the publication of the web service prolific (Senger and Grüning et al., 2012. Mining and evaluation of molecular relationships in literature. Bioinformatics).

- The following table shows the evaluation of the co-occurrences approach (DS - Data set, Sent. - Sentences, Sens. - Sensitivity, Spec. - Specificity, Prec. - Precision, Acc. - Accuracy, F1 - F1 score, evaluation parameters shown in percent):

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - DS
          - #Sent.
          - #CPIs
          - #No-CPIs
          - Total
          - Sens.
          - Spec.
          - Prec.
          - F1

        * - CPI-DS_IV
          - 1209
          - 1598
          - 1269
          - 2867
          - 100.0
          - 0.0
          - 55.7
          - 71.6

        * - CPI-DS_NIV
          - 1404
          - 1333
          - 1362
          - 2695
          - 100.0
          - 0.0
          - 49.5
          - 66.2


- The next table shows the results of the APG kernel pipeline for CPI-DS_IV dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - Param.
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 0.25
          - 82.8
          - 70.0
          - 77.9
          - 77.2
          - 80.1
          - 84.4

        * - 0.50
          - 82.0
          - 70.0
          - 78.0
          - 76.9
          - 79.8
          - 84.5

        * - 1.00
          - 81.2
          - 72.0
          - 78.9
          - 77.1
          - 79.8
          - 84.3

        * - 2.00
          - 80.5
          - 71.3
          - 78.7
          - 76.7
          - 79.4
          - 83.8

- Results of the APG kernel pipeline for CPI-DS_NIV dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - Param.
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 0.25
          - 80.4
          - 69.4
          - 73.4
          - 75.4
          - 76.4
          - 82.2

        * - 0.50
          - 77.9
          - 70.6
          - 73.4
          - 74.6
          - 75.1
          - 82.4

        * - 1.00
          - 75.1
          - 74.3
          - 75.1
          - 75.1
          - 74.9
          - 82.6

        * - 2.00
          - 74.9
          - 74.2
          - 74.7
          - 74.8
          - 74.6
          - 82.8


- This table shows the results of the SL kernel for CPI-DS_IV dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - n
          - w
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 1
          - 1
          - 77.5
          - 67.4
          - 75.7
          - 73.6
          - 76.5
          - 79.4

        * - 1
          - 2
          - 81.3
          - 65.0
          - 75.3
          - 74.7
          - 78.1
          - 79.9

        * - 1
          - 3
          - 80.6
          - 64.3
          - 74.6
          - 74.0
          - 77.4
          - 79.6

        * - 2
          - 1
          - 78.1
          - 70.0
          - 77.3
          - 75.0
          - 77.6
          - 80.8

        * - 2
          - 2
          - 80.5
          - 66.3
          - 75.6
          - 74.6
          - 77.9
          - 80.8

        * - 2
          - 3
          - 80.2
          - 65.8
          - 75.1
          - 74.2
          - 77.5
          - 80.2

        * - 3
          - 1
          - 77.9
          - 71.1
          - 78.0
          - 75.3
          - 77.8
          - 81.3

        * - 3
          - 2
          - 81.2
          - 66.5
          - 76.0
          - 75.1
          - 78.4
          - 81.1

        * - 3
          - 3
          - 80.1
          - 66.9
          - 75.9
          - 74.6
          - 77.8
          - 80.8




- Results of the SL kernel for CPI-DS_NIV dataset:

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - n
          - w
          - Sens.
          - Spec.
          - Prec.
          - Acc.
          - F1
          - AUC

        * - 1
          - 1
          - 78.7
          - 70.7
          - 73.1
          - 74.9
          - 75.6
          - 80.6

        * - 1
          - 2
          - 82.2
          - 64.7
          - 70.2
          - 73.7
          - 75.6
          - 79.7

        * - 1
          - 3
          - 84.0
          - 63.0
          - 69.5
          - 73.6
          - 75.9
          - 79.2

        * - 2
          - 1
          - 78.4
          - 71.7
          - 73.9
          - 75.3
          - 75.9
          - 81.7

        * - 2
          - 2
          - 84.0
          - 63.9
          - 70.3
          - 74.2
          - 76.4
          - 80.9

        * - 2
          - 3
          - 85.0
          - 63.7
          - 70.3
          - 74.5
          - 76.8
          - 80.4

        * - 3
          - 1
          - 80.3
          - 70.5
          - 73.4
          - 75.7
          - 76.6
          - 82.5

        * - 3
          - 2
          - 85.7
          - 63.4
          - 70.4
          - 74.8
          - 77.2
          - 81.8

        * - 3
          - 3
          - 86.7
          - 62.0
          - 69.7
          - 74.5
          - 77.2
          - 81.4




- The ratio of sentences with and without interaction verbs for the complete PubMed data set is around 40 % CPI-DS_IV and 60 % CPI-DS_NIV, based on an analysis with PubMedPortable.

- In the case of CPI-DS_IV and CPI-DS_NIV, the percentages are 46.3 % (1209/(1209+1404)) and 53.7 % (1404/(1209+1404)).

- Considering the manual curation of false positives resulting from the automatic named entity recognition process, the empirical ratios can be considered as similar.

- The predictions for CPI-DS_IV and CPI-DS_NIV are based on training the whole model of CPI-DS, using the same splits. Therefore, the evaluation is separated by the two different sentence structures, but the overall model stays the same for CPI-DS, CPI-DS_IV, and CPI-DS_NIV, regarding each cross-validation run.

The benchmark data set creation
###############################

- The data sets were created by selecting the first 40,000 PubMed abstracts from 2009 with PubMedPortable (https://github.com/KerstenDoering/PubMedPortable).

- The chemical compounds were identified with the backend of prolific using the Hettne rules (Hettne et al., 2009. A dictionary to identify small molecules and drugs in free text. Bioinformatics).

- The web service Whatizit was used for gene and protein synonyms (Rebholz-Schuhmann,D. et al., 2008. Text processing through Web services: calling Whatizit. Bioinformatics).

- After automated extraction of all sentences with an interaction verb (first 20,000 abstracts for CPI-DS_IV) and without an interaction enclosed by two biomolecues (second 20,000 abstracts for CPI-DS_NIV), they were displayed in HTML pages with Javascript buttons to select a status for each sentence.

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

- The script parser.py in the directories scripts/generate_XML_files/CPI-DS_IV/ und scripts/generate_XML_files/CPI-DS_NIV creates the files interactions.txt and no_interactions.txt from the HTML files in the folder data_sets. 

    - The names of these files refer to the basic status of all sentences inside the text file.

    - Relationship_Mining_10000.html and Relationship_Mining_20000.html were concatenated to the file Relationship_Mining.html resulting in CPI-DS_IV. The other two HTML files represent CPI-DS_NIV.

- The script get_relations.py in the directories scripts/generate_XML_files/CPI-DS_IV/ und scripts/generate_XML_files/CPI-DS_NIV processes the files interaction.txt and no_interaction.txt using the (concatenated) file RM_comments.csv with annotations of false positive compounds (FP-C), false positive proteins (FP-P), non-interacting compounds (NI-C), and non-interacting proteins (NI-P).

    - The ouptut of get_relations.py is the file training_dataset.txt.

    - This file can be sorted by PubMed IDs with the command "sort -u training_dataset.txt > training_dataset_sorted.csv", individually done with CPI-DS_IV and CPI-DS_NIV.

- The script annotatedsen_to_xml.py generates the files CPI-DS_IV.xml and CPI-DS_NIV.xml, building a unified XML format described by Tikk et al.

    - This script was developed by Elham Abbasian in her Master Thesis, supervised by Kersten Döring.

- The SL kernel implementation in the ppi-benchmark package of Tikk et al. worked with this XML format, but the preprocessing for the APG kernel-required format did not work straight forward. Therefore, the single steps described in their documentation appendix (here: scripts/ppi-benchmark/documentationkernels-howto.pdf) were isolated from the available source code and stored as executable JAR files in the folder scripts/CPI-corpora-preparing with Eclipse.

- The XML files can be checked for consistency. Furthermore, it can be seen how many documents (PubMed IDs) and sentences there are:

    java -jar ConsistencyChecker.jar CPI-DS_IV/CPI-DS_IV.xml 

        INFO: Processing 'CPI-DS_IV/CPI-DS_IV.xml'...

        Processing corpus 'CPI-DS_IV' ...

        Documents seen: 802

        Sentences seen: 1209


    java -jar ConsistencyChecker.jar CPI-DS_NIV/CPI-DS_NIV.xml 

        INFO: Processing 'CPI-DS_NIV/CPI-DS_NIV.xml'...

        Processing corpus 'CPI-DS_NIV' ...

        processed 1000 docs (2155.1724 docs/sec)

        Documents seen: 1006

        Sentences seen: 1404


    java -jar ConsistencyChecker.jar DS_40/DS-40.xml 

        INFO: Processing 'DS_test_case_40_sentences/DS-40.xml'...

        Processing corpus 'DS-40' ...

        Documents seen: 26

        Sentences seen: 40


Technical Requirements for running APG and SL Kernel Pipeline
*************************************************************

- Many of the following steps are described similarly in the original ppi-benchmark documentation (scripts/ppi-benchmark/documentationkernels-howto.pdf).


Required Installation Packages
##############################

- The operating system for the CPI-pipeline was Ubuntu 14.04 LTS and the whole pipeline was tested with Ubuntu 16.04 LTS & Ubuntu 18.04 LTS.

- All packages can be installed with "apt-get install", Synaptic Package Manager, or the new Ubuntu Software Center.

- List of packages:

    - Python 2.7

    - postgresql (here: version 9.3, used to store evaluation results)

    - libxml-perl (here: version 0.08, used for the generation of cross-validation splits)

    - python-lxml

    - python-numpy

    - default-jdk (Java 7 or 8, used for the execution of JAR files)

    - python-nltk

    - python-pip

    - pip install bllipparser (python bindings for the BLLIP natural language parser)


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

        - localhost:\*:ppi:ppi:ppi

        - EOF

- Create the tables which are needed for uploading the results. Change into scripts/ppi-benchmark/Database and execute the following command:

    - psql -h localhost -d ppi -U ppi -f init-ppiCV.sql 


How to run the Kernel Pipelines
*******************************

- This section describes how to use run the APG and SL kernel with the combined data set (CPI-DS), CPI-DS_IV, and CPI-DS_NIV in different modes:

    - CV: 10x-cross-validation

    - PR: prediction, based on the trained model of the combined data set (CPI-DS) 

    - XX: cross-corpus training and prediction on user-specific data sets

- Furthermore, it contains a short paragraph about how to use these models.

APG Kernel pipeline
###################

- These are the 3 main commands:
 
    - CV: make experiment Kernel=APG expTyp=CV InputFile=CPI-DS.xml Processors=4
 
    - PR: make experiment Kernel=APG expTyp=PR InputFile=CPI-DS.xml Processors=4
 
    - XX: make experiment Kernel=APG expTyp=XX TrainFile=train.xml TestFile=test.xml Processors=4

- You can use the test data set DS-40.xml with 40 sentences to check whether your pipeline works. 

- While the complete CPI-DS_IV pipeline runs around 3:40 h, the test case takes only a few minutes on a notebook with an Intel Core i5-6500 (4x 3.20GHz).

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

- In "scripts/ppi-benchmark/Experiments/APG/PR/predict/CPI-DS/train0000/predict1.out", you will find the test predictions with the original class in the second column and the complete sentence identifier in the first column (for the lambda value 1).

- In "scripts/ppi-benchmark/Experiments/APG/PR/predict/CPI-DS/train0000/threshold1.out", you will find the train predictions (self-prediction) for the F1 score optimization with the original class in the second column and the complete sentence identifier in the first column (for the lambda value 1).

- The file scripts/ppi-benchmark/Experiments/APG/PR/output.sql contains all prediction values (0 for false, and 1 for true, and the prediction value itself).

SL Kernel pipeline
##################

- These are the 3 main commands:
 
    - CV: make experiment Kernel=SL expTyp=CV InputFile=CPI-DS.xml Processors=4
 
    - PR: make experiment Kernel=SL expTyp=PR InputFile=CPI-DS.xml Processors=4
 
    - XX: make experiment Kernel=SL expTyp=XX TrainFile=train.xml TestFile=test.xml Processors=4

- You can clean your SL workspace after a calculation is finished:

    - make clean-SL

- Or you can clean the whole workspace:

    - make clean-all

- The input files need to be located in "scripts/generate_XML_files/DS".

- Ammar Qaseem updated and completely refined the first version of this pipeline to be used in three modes (cross-validation, prediction, cross-corpus) with only one script SL_Pipeline.sh.

- Michael Becer was involved in developing a previous version of an independently customized pipeline using the SL kernel as part of his Bachelor Thesis, supervised by Kersten Döring.

- Kevin Selm wrote a bugfix for the jSRE software, because it was not possible to use different parameter selections of n and w. 

    - Original software link: 

        - https://hlt-nlp.fbk.eu/technologies/jsre

- The ppi-benchmark pipeline was changed to make use of the JAR file scripts/ppi-benchmark/Kernels/jsre/source/dist/runTrain.jar, which was exported from a newly created Eclipse project with the source code of the original software and the debugged code of Kevin Selm.

    - You can find these files in the folder scripts/jSRE_debug.

- The complete CPI-DS_IV pipeline runs in around 0:18 h with an Intel Core i5-6500 (4x 3.20GHz).

- The threshold for a positive or negative prediction is zero and stored in the SQL database.


- In "scripts/ppi-benchmark/Experiments/SL/PR/predict/CPI-DS/train0000/predictn=3w=1.out", you will find the predictions with the original class in the second column and the complete sentence identifier in the first column (for n=3 and w=1).

- The file scripts/ppi-benchmark/Experiments/SL/PR/output.sql contains all prediction values (0 for false, and 1 for true, and the prediction value itself).

Data set evaluation
###################

- The folder results/summary/*<nameOfKernel>*/*<nameOfDataset>*/output/ contains scripts to evaluate the results (numbers shown in the tables in the section "Introduction").

- If you want to repeat the evaluation procedure, execute the following steps:

    - Remove all files in the folder output, except average.py and header.py and then run:

    - ./get_results.sh


- *nameOfKernel* is the name of the kernel (SL or APG) and *nameOfDataset* is the name of the dataset(CPI-DS, CPI-DS_IV, or CPI-DS_NIV) .


- Check the files CPI-DS_average_header.csv, CPI-DS_IV_average_header.csv, and CPI-DS_NIV_average_header.csv. They exist as a backup in the folder results/summary/*<nameOfKernel>*/*<nameOfDataset>*/final/ and the selected SQL results are stored as a backup in the folder results/summary/*<nameOfKernel>*/*<nameOfDataset>*/backup_original.


- You can reproduce any APG cross-validation run by commenting out lines 188 and 189 in scripts/APG_Pipeline.sh and copying your selected cross-validation splits to CPI-corpora-preparing/splitting/DS.

- You can reproduce any SL cross-validation run by commenting out lines 205-207 in scripts/ppi-benchmark/Corpora/Makefile and line 93 in scripts/SL_Pipeline.sh. You also need to copy your selected cross-validation splits to ppi-benchmark/Corpora/Splits/DS.

- If you want to reproduce the cross-validation results of CPI-DS_IV and CPI-DS_NIV, please, have a look at the readme files in "scripts/splitting/scripts_for_use_same_splits".

Usage of Created Models
#######################

- If you want to use the models created with any data set, use the XX mode. If you want to use our representative model of PubMed, run the PR mode.

- You can use PubMedPortable with its named entity recognition interfaces to prepare sentences with highlighted compounds and proteins.

- The basic input for the script annotatedsen_to_xml.py (training_dataset_sorted.csv) can be created by generating a tab-separated format which contains the following columns:

    - PubMed ID

    - Sentence with XML tags for all named entities

    - As many more columns as there are pairs of related entities

        - Format of each pair: <entity>__<entity>__<interaction>

- This format will automatically be generated with the following example command in the folder "scripts/annotate_entities" (further explanations in the "scripts/annotate_entities/how_to" file):

    - make annotate InputFile=pmid_example/pmid_example OutputFile=annotate_res.txt Processors=2

- You will need to configure python-nltk to download the punkt tokenizer before:

    - cd ~

    - mkdir nltk_data

    - ipython

    - import nltk

    - nltk.download_shell()

    - d

    - punkt

    - q

- The example output of this file, converted to an XML file (with the script annotatedsen_to_xml.py as described in the section "Technical background of the XML data set"), is "scripts/generate_XML_files/DS/annotate_res.xml".

- Considering the output of such an experiment, all positively predicted pairs of entities can be used for an ongoing analysis, e.g. in the process of filtering out interaction partners from large-scale corpora.

- If you want to run your own model in the PR mode, you need to copy files from your XX run to specific directories.

- In the case of the SL kernel, you need to copy the .model file from "scripts/ppi-benchmark/Experiments/SL/XX/trained/DS/train0" to "scripts/training_model/SL_PR_training/trained_model/DS/train0".

- In the case of the APG kernel, there are more steps:

    - Copy your .model file from "scripts/ppi-benchmark/Experiments/APG/XX/trained/DS/train0" to "scripts/training_model/APG_PR_training/trained_model/DS/train0".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/corpus/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/corpus_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/dictionary/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/dict_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/linearized/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/linearized_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/normalized/DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/normalized_train0.txt.gz".

- Running both kernels in PR mode, one after the other, will generate the files "scripts/ppi-benchmark/Experiments/SL/PR/output.sl.xml" and "scripts/ppi-benchmark/Experiments/APG/PR/output.apg.xml".

- Analogously, the same happens in the XX mode.

- Regarding the XX mode, the default parameter for the APG kernel is c=1. You can change it by entering your desired value to "scripts/Run_APG_Kernel.py" in line 257, where c0 = 0 will be used as 2^0 = 1. If you want your model to take e.g. c=2, you have to set c0 = 1, because 2^1 = 2.

- You can do the same for the XX mode with the SL kernel by changing "scripts/Run_SL_Kernel.py" lines 88 and 90. The parameters w0 and n0 will be taken as you set them. The default is n=3 and w=1.

- These files will have the same content as the input xml file, e.g. annotate_res.xml, except that each positively predicted compound-protein pair will be annotated with 'interaction="True"'.

- All compound-protein pairs which were predicted as non-functional relationships will keep their default annotation 'interaction="False"'.

- The comparison of the predictions of both kernels (output.sl.xml and output.apg.xml) can be used to make a jury decision, resulting in a high confidence for identical outputs.



Large-scale dataset application
********************************

The kernels have been successfully applied to all PubMed titles and abstracts that were published before July 2019. The full output (in xml format) can be found here: 

	- ftp://132.230.56.164/CPI/

It contains one zip file for the predictions of each of the two kernels (SL and APG) as well as one zip file with the combination of both kernels based on a jury decision, i.e. only those relations that were predicted as a functional relation by both kernels were classified to be positive.

Benchmark dataset
******************
The full benchmark dataset as an XML file can also be found here : 

	- ftp://132.230.56.164/CPI/


Interaction verbs
******************
These verbs have been defined in the publication of the web service prolific (Senger and Grüning et al., 2012. Mining and evaluation of molecular relationships in literature. Bioinformatics). This list can be found here : 

	- ftp://132.230.56.164/CPI/


Contact
*******

- Please, write an e-mail, if you have questions, feedback, improvements, or new ideas:

    - kersten.doering@gmail.com

    - ammar.qaseem@pharmazie.uni-freiburg.de

- If you are interested in related projects, visit our working group's homepage:

    - http://www.pharmbioinf.uni-freiburg.de/


License
#######

- The CPI-Pipeline project is published with an ISC license given in "license.txt".
