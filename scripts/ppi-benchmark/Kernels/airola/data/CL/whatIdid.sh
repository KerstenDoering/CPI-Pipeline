#These corpora were semi-manually generated

File Edit Options Buffers Tools Insert Help                                                                                                                  
wget http://mars.cs.utu.fi/PPICorpora/AImed-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/BioInfer-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/HPRD50-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/IEPA-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/LLL-learning-format.xml.gz

gunzip *.gz

mkdir AImed; mkdir BioInfer; mkdir HPRD50; mkdir IEPA; mkdir LLL;
cp AImed-learning-format.xml AImed/test.xml
cp BioInfer-learning-format.xml BioInfer/test.xml
cp HPRD50-learning-format.xml HPRD50/test.xml
cp IEPA-learning-format.xml IEPA/test.xml
cp LLL-learning-format.xml LLL/test.xml


cat BioInfer-learning-format.xml HPRD50-learning-format.xml IEPA-learning-format.xml LLL-learning-format.xml > AImed/train.xml
cat AImed-learning-format.xml HPRD50-learning-format.xml IEPA-learning-format.xml LLL-learning-format.xml  > BioInfer/train.xml
cat AImed-learning-format.xml BioInfer-learning-format.xml IEPA-learning-format.xml LLL-learning-format.xml > HPRD50/train.xml
cat AImed-learning-format.xml BioInfer-learning-format.xml  HPRD50-learning-format.xml LLL-learning-format.xml > IEPA/train.xml
cat AImed-learning-format.xml BioInfer-learning-format.xml HPRD50-learning-format.xml IEPA-learning-format.xml > LLL/train.xml
rm *.xml

#change all train-files
find -name train.xml -exec emacs -nw {} \;
