mkdir corpus
mkdir corpus/AImed
mkdir corpus/BioInfer
mkdir corpus/HPRD50
mkdir corpus/IEPA
mkdir corpus/LLL

cat ../CV/parsed/AImed/test*  > corpus/AImed/corpus.txt
cat ../CV/parsed/BioInfer/test* > corpus/BioInfer/corpus.txt
cat ../CV/parsed/HPRD50/test* > corpus/HPRD50/corpus.txt
cat ../CV/parsed/IEPA/test* > corpus/IEPA/corpus.txt
cat ../CV/parsed/LLL/test* > corpus/LLL/corpus.txt
