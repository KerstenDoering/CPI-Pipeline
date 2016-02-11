wget http://mars.cs.utu.fi/PPICorpora/AImed-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/BioInfer-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/HPRD50-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/IEPA-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/LLL-learning-format.xml.gz



mkdir AImed; mkdir  BioInfer; mkdir  HPRD50;  mkdir IEPA; mkdir   LLL;
mv AImed-learning-format.xml.gz AImed/corpus.xml.gz
mv BioInfer-learning-format.xml.gz BioInfer/corpus.xml.gz
mv HPRD50-learning-format.xml.gz HPRD50/corpus.xml.gz
mv IEPA-learning-format.xml.gz IEPA/corpus.xml.gz
mv LLL-learning-format.xml.gz LLL/corpus.xml.gz

mkdir corpus
mv AImed/ corpus/
mv BioInfer/ corpus/
mv HPRD50/ corpus/
mv IEPA/ corpus/
mv LLL/ corpus/
