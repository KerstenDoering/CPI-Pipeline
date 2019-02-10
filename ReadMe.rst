Compound-Protein Interaction Pipeline
=====================================


Introduction
************

- The presented pipeline uses the protein-protein interaction benchmark package published by Tikk et al. (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).

- The selection of considered kernels and software components was reduced to the all-paths graph (APG) kernel and the shallow linguistic (SL) kernel, because they performed best on the protein-protein interaction (PPI) data sets.

- In this project, the two kernels were applied to two compound-protein interaction (CPI) in PubMed sentences.

- The complete data set consists of 2753 sentences. Within these sentences, 3496 compound-protein pairs were annotated to show a functional relationship and 2467 compound-protein pairs were marked as no-interaction pairs.

- We consider co-occurences as an approach to predict every appearance of a compound and a protein in a sentence as a functional relationship (recall 100%, specificity 0%) and call it the baseline calculation, taking into account the number of true functional relationships.

- From the given numbers, the data set shows an precision (equal to accuracy in this case) of 58.6 % and an F1 score of 73.9 %.

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
          - 85.0
          - 65.3
          - 77.8
          - 77.0
          - 81.2
          - 84.1

        * - 0.50
          - 84.6
          - 65.8
          - 77.9
          - 77.0
          - 81.1
          - 84.1

        * - 1.00
          - 84.0
          - 67.0
          - 78.4
          - 77.2
          - 81.1
          - 83.8

        * - 2.00
          - 84.2
          - 66.4
          - 78.1
          - 77.0
          - 81.0
          - 83.4


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
          - 77.1
          - 68.6
          - 77.9
          - 73.6
          - 77.4
          - 79.1

        * - 1
          - 2
          - 83.0
          - 61.1
          - 75.4
          - 74.0
          - 78.9
          - 78.6

        * - 1
          - 3
          - 87.1
          - 53.0
          - 72.5
          - 73.0
          - 79.1
          - 78.1

        * - 2
          - 1
          - 79.0
          - 68.8
          - 78.3
          - 74.8
          - 78.6
          - 80.9

        * - 2
          - 2
          - 84.5
          - 60.8
          - 75.5
          - 74.7
          - 79.7
          - 80.3

        * - 2
          - 3
          - 87.9
          - 54.8
          - 73.7
          - 74.3
          - 80.1
          - 79.9

        * - 3
          - 1
          - 80.3
          - 68.7
          - 78.5
          - 75.5
          - 79.3
          - 81.4

        * - 3
          - 2
          - 84.4
          - 62.0
          - 76.1
          - 75.2
          - 80.0
          - 80.8

        * - 3
          - 3
          - 88.2
          - 56.3
          - 74.3
          - 75.1
          - 80.6
          - 80.6

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
          - 1259
          - 1884
          - 1166
          - 3050
          - 100.0
          - 0.0
          - 61.8
          - 76.4

        * - CPI-DS_NIV
          - 1494
          - 1612
          - 1301
          - 2913
          - 100.0
          - 0.0
          - 55.3
          - 71.2


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
          - 85.4
          - 59.6
          - 78.4
          - 76.3
          - 81.7
          - 81.7

        * - 0.50
          - 85.0
          - 59.8
          - 78.4
          - 76.1
          - 81.5
          - 81.6

        * - 1.00
          - 84.4
          - 60.9
          - 79.0
          - 76.3
          - 81.6
          - 81.4

        * - 2.00
          - 84.6
          - 60.1
          - 78.5
          - 76.0
          - 81.4
          - 81.0

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
          - 84.3
          - 69.0
          - 77.3
          - 77.5
          - 80.5
          - 85.6

        * - 0.50
          - 84.1
          - 69.9
          - 77.7
          - 77.8
          - 80.6
          - 85.5

        * - 1.00
          - 83.5
          - 70.9
          - 78.1
          - 77.8
          - 80.6
          - 85.4

        * - 2.00
          - 83.7
          - 70.2
          - 77.8
          - 77.7
          - 80.6
          - 85.0


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
          - 78.8
          - 60.4
          - 76.5
          - 71.9
          - 77.5
          - 75.5

        * - 1
          - 2
          - 82.2
          - 55.2
          - 75.1
          - 72.1
          - 78.3
          - 74.8

        * - 1
          - 3
          - 86.7
          - 46.7
          - 72.6
          - 71.6
          - 78.9
          - 74.6

        * - 2
          - 1
          - 79.9
          - 61.1
          - 77.1
          - 72.9
          - 78.3
          - 77.3

        * - 2
          - 2
          - 84.0
          - 54.2
          - 74.9
          - 72.7
          - 79.0
          - 76.7

        * - 2
          - 3
          - 88.3
          - 47.6
          - 73.2
          - 72.8
          - 79.9
          - 76.4

        * - 3
          - 1
          - 81.1
          - 61.7
          - 77.8
          - 74.0
          - 79.3
          - 78.3

        * - 3
          - 2
          - 83.5
          - 56.8
          - 76.2
          - 73.7
          - 79.6
          - 77.5

        * - 3
          - 3
          - 88.5
          - 50.7
          - 74.7
          - 74.3
          - 80.9
          - 77.4




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
          - 75.5
          - 74.8
          - 78.9
          - 75.3
          - 77.1
          - 81.9

        * - 1
          - 2
          - 82.7
          - 67.3
          - 76.0
          - 75.9
          - 79.1
          - 81.4

        * - 1
          - 3
          - 87.4
          - 58.3
          - 72.3
          - 74.4
          - 79.0
          - 80.9

        * - 2
          - 1
          - 78.3
          - 75.0
          - 79.6
          - 76.8
          - 78.8
          - 83.6

        * - 2
          - 2
          - 84.2
          - 69.0
          - 77.4
          - 77.4
          - 80.5
          - 83.1

        * - 2
          - 3
          - 87.6
          - 62.5
          - 74.5
          - 76.4
          - 80.4
          - 82.9

        * - 3
          - 1
          - 79.7
          - 74.5
          - 79.6
          - 77.4
          - 79.5
          - 84.0

        * - 3
          - 2
          - 84.2
          - 68.6
          - 77.1
          - 77.2
          - 80.4
          - 83.5

        * - 3
          - 3
          - 88.6
          - 62.4
          - 74.7
          - 76.9
          - 80.9
          - 83.3




- The ratio of sentences with and without interaction verbs for the complete PubMed data set is around 40 % CPI-DS_IV and 60 % CPI-DS_NIV, based on an analysis with PubMedPortable.

- In the case of CPI-DS_IV and CPI-DS_NIV, the percentages are 45.7 % (1259/(1259+1494)) and 54.3 % (1494/(1259+1494)).

- Considering the manual curation of false positives resulting from the automatic named entity recognition process, the empirical ratios can be considered as similar.

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

        Documents seen: 830

        Sentences seen: 1259


    java -jar ConsistencyChecker.jar CPI-DS_NIV/CPI-DS_NIV.xml 

        INFO: Processing 'CPI-DS_NIV/CPI-DS_NIV.xml'...

        Processing corpus 'CPI-DS_NIV' ...

        processed 1000 docs (2155.1724 docs/sec)

        Documents seen: 1066

        Sentences seen: 1494


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

    - postgresql (here: version 9.3, used to store evaluation results)

    - libxml-perl (here: version 0.08, used for the generation of cross-validation splits)

    - python-numpy (here: using Python 2.7, used within the make experiment steps)

    - default-jdk (Java 7 or 8, used for the execution of JAR files)

    - python-nltk

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

- While the complete CPI-DS_IV pipeline runs around 3:15 h, the test case takes only a few minutes on a notebook with an Intel Core i5-3570 (4x 3.40GHz).

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

- The complete CPI-DS_IV pipeline runs in around 0:14 h with an Intel Core i5-3570 (4x 3.40GHz).

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

- If you want to run your own models in the PR mode, you need to copy files from your XX run to specific directories.

- In the case of the SL kernel, you need to copy the .model file from "scripts/ppi-benchmark/Experiments/SL/XX/trained/DS/train0" to "scripts/training_model/SL_PR_training/trained_model/CPI-DS/train0".

- In the case of the APG kernel, there are more steps:

    - Copy your .model file from "scripts/ppi-benchmark/Experiments/APG/PR/trained/CPI-DS/train0" to "scripts/training_model/APG_PR_training/trained_model/CPI-DS/train0".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/corpus/CPI-DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/corpus_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/dictionary/CPI-DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/dict_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/linearized/CPI-DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/linearized_train0.txt.gz".

    - Copy "scripts/ppi-benchmark/Experiments/APG/XX/normalized/CPI-DS/train0.txt.gz" to "scripts/training_model/APG_PR_training/normalized_train0.txt.gz".

- Running both kernels in PR mode, one after the other, will generate the files "scripts/ppi-benchmark/Experiments/SL/PR/output.sl.xml" and "scripts/ppi-benchmark/Experiments/APG/PR/output.apg.xml".

- These files will have the same content as the input xml file, e.g. annotate_res.xml, except that each positively predicted compound-protein pair will be annotated with 'interaction="True"'.

- All compound-protein pairs which were predicted as non-functional relationships will keep their default annotation 'interaction="False"'.

- The comparison of the predictions of both kernels (output.sl.xml and output.apg.xml) can be used to make a jury decision, resulting in a high confidence for identical outputs.


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
