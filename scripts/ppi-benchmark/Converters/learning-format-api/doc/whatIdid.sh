#0.) Download all 5 corpora into folder original
wget http://mars.cs.utu.fi/PPICorpora/AImed-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/BioInfer-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/HPRD50-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/IEPA-learning-format.xml.gz
wget http://mars.cs.utu.fi/PPICorpora/LLL-learning-format.xml.gz

gunzip *.gz

#For das File ein $PWD/$file
#1) 
#Extracts sentences from the original XML 
#Result is written in $file-ptb-s.txt
for file in *.xml
do
    java -classpath $HOME/workspace/learning-format-api/bin/ org.learningformat.transform.PtbRawSentenceTransformer $file
done

#2.) Parsing
#Results in two files -parsed.txt and -parsed.err
for file in *-ptb-s.txt; 
do
    ~/Desktop/svm/training/reranking-parser/parse.sh $file > $file-parsed.txt 2>$file-parsed.err; 
done

#Also exectuted it on racer:
#To check if the results are similar between the two parses
#/vol/home-vol3/wbi/thomas/tmp/parsingTest/original

mkdir charniak-johnson
mv *-parsed.* charniak-johnson/
mkdir trees


#3.)Combine XML and PTB together
# Input is the original XML
# Requires the  corresponding file in directory "charniak-johnson" with file extension  "-ptb-s.txt-parsed.txt" 
#Writes into trees
for file in $PWD/*.xml; 
do 
    java  -classpath $HOME/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/lib/jargs.jar org.learningformat.transform.PtbTreeInjector -f $file -o `dirname $file`/trees/`basename $file`  -i;
done

#4.)Generates a mapping between POS and ??real text??
# Input is the XML-File in folder "trees"
# Writes output in the folder "trees" suffix "-bracketing-tokens.txt" in folder 
for file in $PWD/trees/*.xml; 
do
    java  -classpath /home/philippe/workspace/learning-format-api/bin/ org.learningformat.transform.BracketingTokenMapper $file
done

# 5.) Needs folder mapped trees,  because it stores results there
#Important InjectTreees=FALSE
#needs parametrization

mkdir trees/mapped-trees
for file in $PWD/trees/*.xml;
do
    java  -classpath /home/philippe/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/lib/jargs.jar org.learningformat.transform.PtbTreeInjector -f $file  -o `dirname $file`/mapped-trees/`basename $file`;
done




#6.) Create final splits 
#Needs final XML-Files in folder "trees/mapped-trees"
#Result is written into folder "$PWD/Corpora/" and then Moschitti or Custom
mkdir corpora


for file in $PWD/trees/mapped-trees/*.xml; 
do
    java -classpath /home/philippe/workspace/learning-format-api/bin/:$HOME/workspace/learning-format-api/lib/jargs.jar org.learningformat.transform.SvmLightTreeKernelTransformer  -f $file -m -s $HOME/Desktop/svm/learning/splits -o $PWD/corpora;
done

