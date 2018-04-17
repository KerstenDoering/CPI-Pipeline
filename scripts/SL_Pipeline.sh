
#    Copyright (c) 2015-2017, Kersten Doering <kersten.doering@gmail.com>, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>
#    Copyright (c) 2018, Ammar Qaseem <ammar.qaseem@pharmazie.uni-freiburg.de>, Kersten Doering <kersten.doering@gmail.com>

#    This script executes the steps from the protein-protein-interaction pipeline of Tikk et al. (scripts/ppi-benchmark/Documentation/kernels-howto.pdf, (Tikk et al., 2010. A comprehensive benchmark of kernel methods to extract protein-protein interactions from literature. PLoS Comput. Biol).


VERSION=0.1

usage="$(basename "$0") [-h] [-f] [-x] [-p n] -- This script to identify the functional Compound-Protein relationships

where:
    -h  help.
    -f  Input file (default: DS.xml).
    -t  Type of experiment (CV, PR, XX).
    -x  Type of process(Train or test). This parameter just used with XX.
    -p  Number of processors (default: 2)."


#filename="DS.xml"
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

baseDir=$(pwd)"/ppi-benchmark"

sed -i 's|^baseDir=.*|baseDir='"$baseDir"'|g' ppi-benchmark/Makefile.config
sed -i 's|^KERNELS=.*|KERNELS=SL|g' ppi-benchmark/Makefile.config
sed -i 's|^EXPTYPES=.*|EXPTYPES='"$ExpTyp"'|g' ppi-benchmark/Makefile.config


mkdir -p ppi-benchmark/Corpora/Original
mkdir -p ppi-benchmark/Corpora/Original-Modified

cp generate_XML_files/DS/DS.xml ppi-benchmark/Corpora/Original

# change into the (just prepared folders from the all-paths graph kernel directory)
cd ppi-benchmark/Corpora/Original
# ToDo: use copy command to get files from generate_XML_files
cp DS.xml ../Original-Modified 
cd ..

rm -rf SL
# if there are files from a previous shallow linguistic kernel run, they will be removed 
rm -rf Splits/DS/


if [ $ExpTyp = "XX" ] && [ $ProcessTyp = "train" ]
then

   make generate-enriched-xml
   make create-SL-LF
   cat SL/training-format/XX/corpus/DS/* > train0.txt
   exit 0 # for training process, we need just the pre-processing steps
fi


# change into directory Experiments to start the calculation and the upload process
cd ../Experiments
pwd
echo "run SL pipeline ..."
mkdir -p SL/$ExpTyp/
cp ../../Run_SL_Kernel.py SL/$ExpTyp/run.py

make experiment Corpora="DS" Kernel="SL" expType=$ExpTyp


echo "uploading results to PostgreSQL ..."
make output2db Corpora="DS" Kernel="SL" expType=$ExpTyp
cd ..
cd Database

psql -h localhost -d ppi -U ppi -f manage_folds.sql

#return to the start directory and show the time at which this pipeline ended
cd ../..
echo "calculation ended at " $(date +"%T")
