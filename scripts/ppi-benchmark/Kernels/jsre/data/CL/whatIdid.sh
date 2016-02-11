
mkdir corpus/AImed; mkdir corpus/BioInfer; mkdir corpus/HPRD50; mkdir corpus/IEPA; mkdir corpus/LLL

cat ../../run/corpus/BioInfer/test* ../../run/corpus/HPRD50/test* ../../run/corpus/IEPA/test* ../../run/corpus/LLL/test* >AImed/train.txt 
cat ../../run/corpus/AImed/test* ../../run/corpus/HPRD50/test* ../../run/corpus/IEPA/test* ../../run/corpus/LLL/test* > BioInfer/train.txt
cat ../../run/corpus/AImed/test* ../../run/corpus/BioInfer/test* ../../run/corpus/IEPA/test* ../../run/corpus/LLL/test* > HPRD50/train.txt
cat ../../run/corpus/AImed/test* ../../run/corpus/BioInfer/test* ../../run/corpus/HPRD50/test* ../../run/corpus/LLL/test* > IEPA/train.txt
cat ../../run/corpus/AImed/test* ../../run/corpus/BioInfer/test* ../../run/corpus/HPRD50/test* ../../run/corpus/IEPA/test* > LLL/train.txt


cat ../../run/corpus/AImed/test* > AImed/test.txt
cat ../../run/corpus/BioInfer/test* > BioInfer/test.txt
cat ../../run/corpus/HPRD50/test* > HPRD50/test.txt
cat ../../run/corpus/IEPA/test* > IEPA/test.txt
cat ../../run/corpus/LLL/test* > LLL/test.txt
