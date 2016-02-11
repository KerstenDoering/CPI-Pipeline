mkdir tmp
cd tmp

#0.) Download all 5 corpora into folder original
wget http://mars.cs.utu.fi/PPICorpora/AImed-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/BioInfer-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/HPRD50-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/IEPA-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/LLL-learning-format.xml.gz

gunzip *.gz


#1.) Extract each token of a sentence
#a.) for "split"
for file in *.xml; 
do
     java -classpath /home/philippe/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/src/main/resources/jargs.jar org.learningformat.transform.JSRE_TrainingFormatConverter -o out/  -t split split -i $file; 
done

#b.) for "charniak lease" 
for file in *.xml; 
do
     java -classpath /home/philippe/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/src/main/resources/jargs.jar org.learningformat.transform.JSRE_TrainingFormatConverter -o out/  -t Charniak-Lease -i $file; 
done

find out/* -exec cat {} >> out/tst.txt \;


#2.) Lemmatization of the relevant sentences; (performed on racer)
#scp out/tst.txt racer:/vol/home-vol3/wbi/thomas/tmp/
export TEXTPRO=/vol/home-vol3/wbi/thomas/tmp/TextPro/TextPro1.4
perl ~/tmp/TextPro/TextPro1.4/textpro -no_abstract_lemma -d token+sentence -l eng -c token+lemma tst.txt
#scp racer:/vol/home-vol3/wbi/thomas/tmp/tst.txt.txp  .


#Return the lemmatas for each word
#split
#perl ~/tmp/TextPro/TextPro1.4/textpro -no_abstract_lemma -d token+sentence -l eng -c token+lemma /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre/corpus/out/split/

#Charniak Lease
#perl ~/tmp/TextPro/TextPro1.4/textpro -no_abstract_lemma -d token+sentence -l eng -c lemma /vol/home-vol3/wbi/thomas/backup/svm/otherMethods/jsre/corpus/out/Charniak-Lease/


#3.)Build the CV-training format
for file in *.xml; 
do
    java -classpath /home/philippe/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/src/main/resources/jargs.jar org.learningformat.api.JSRE_Tranformer \
    -s /home/philippe/workspace/Kernels/jsre/data/split \
    -o /home/philippe/workspace/Kernels/jsre/data/CV/parsed \
    -l /home/philippe/workspace/Kernels/jsre/data/CV/tmp/tst.txt.txp \
    -i $file
done

cd ..
rm -rf tmp/